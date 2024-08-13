"""Generator.

This module provides all facilities to create documentation.
"""

import json
import os
import subprocess
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

from pydantic import create_model

from cyberfusion.RabbitMQConsumer.contracts import (
    RPCRequestBase,
    RPCResponseBase,
)
from cyberfusion.RabbitMQConsumer.processor import MESSAGE_ERROR
from cyberfusion.RabbitMQConsumer.utilities import (
    get_exchange_handler_class_request_model,
    get_exchange_handler_class_response_model,
    import_installed_handler_modules,
)

KEY_EXAMPLES = "examples"
NAME_SCHEMA_HEAD = "head"


@dataclass
class ExchangeToClassesMapping:
    """Mapping from specific exchange to its request and response classes."""

    exchange_name: str
    request_model: RPCRequestBase
    response_model: RPCResponseBase


def _create_schemas_directory() -> str:
    """Create directory which contains JSON schemas."""
    path = os.path.join(os.path.sep, "tmp", "schemas-" + str(uuid.uuid4()))

    os.mkdir(path)

    return path


def _create_documentation_directory() -> str:
    """Create directory which contains documentation (HTML based on JSON schemas)."""
    path = os.path.join(os.path.sep, "tmp", "result-" + str(uuid.uuid4()))

    os.mkdir(path)

    return path


def _inject_default_examples(
    response_model: RPCResponseBase,
) -> RPCResponseBase:
    """Add the default error response to response examples."""
    if KEY_EXAMPLES not in response_model.Config.schema_extra:
        response_model.Config.schema_extra[KEY_EXAMPLES] = []

    response_model.Config.schema_extra[KEY_EXAMPLES].append(
        {
            "_description": "Uncaught error",
            "success": False,
            "message": MESSAGE_ERROR,
            "data": None,
        }
    )

    return response_model


def _create_exchange_to_classes_mappings() -> List[ExchangeToClassesMapping]:
    """Map all exchanges to their request and response classes."""
    mappings = []

    modules = import_installed_handler_modules()

    for module in modules:
        request_model = get_exchange_handler_class_request_model(
            module.Handler
        )
        response_model = get_exchange_handler_class_response_model(
            module.Handler
        )

        response_model = _inject_default_examples(response_model)

        mappings.append(
            ExchangeToClassesMapping(
                exchange_name=module.__name__,
                request_model=request_model,
                response_model=response_model,
            )
        )

    return mappings


def _create_exchange_to_model_schemas(
    schemas_directory: str,
    exchange_to_classes_mappings: List[ExchangeToClassesMapping],
) -> List[str]:
    """Create exchange to model mapping (which request/response models belong to which exchange)."""
    models = []
    schema_files = []

    # Construct models

    for mapping in exchange_to_classes_mappings:
        model = create_model(
            mapping.exchange_name,
            request_model=(mapping.request_model, ...),
            response_model=(mapping.response_model, ...),
        )

        models.append(model)

    # Write schemas of models to files

    for model in models:
        schema_file = os.path.join(schemas_directory, model.__name__) + ".json"

        with open(schema_file, "w") as f:
            json_schema = model.schema_json()

            f.write(json_schema)

        schema_files.append(schema_file)

    return schema_files


def _create_head_schema(
    schema_files: List[str], schemas_directory: str
) -> str:
    """Create head schema.

    This schema contains references to all JSON schemas, thereby including all
    JSON schemas without the need to merge them.
    """

    # Construct schema

    head_schema: Dict[str, List[Dict[str, str]]] = {"allOf": []}

    for schema_file in schema_files:
        head_schema["allOf"].append({"$ref": schema_file})

    # Write schema

    path = os.path.join(schemas_directory, NAME_SCHEMA_HEAD + ".json")

    with open(path, "w") as f:
        f.write(json.dumps(head_schema))

    return path


def _create_documentation(schema: str, schemas_directory: str) -> str:
    """Create documentation (HTML based on JSON schemas)."""

    # json-schema-for-humans provides a Python API, but not for creating
    # documentation for multiple schemas, while the CLI does. The methods
    # that the CLI uses are not private, but not documented either, so
    # using the CLI is a more stable option.

    subprocess.check_output(
        [
            "generate-schema-doc",
            "--config",
            "template_name=js_offline",
            schema,
            schemas_directory,
        ]
    )

    return Path(schema).stem + ".html"


def generate_documentation() -> Tuple[str, str, str]:
    """Generate HTML documentation for exchanges' request and response models."""
    schemas_directory = _create_schemas_directory()
    documentation_directory = _create_documentation_directory()

    # For every exchange, create schemas for its request and response models

    exchange_to_classes_mappings = _create_exchange_to_classes_mappings()
    schema_files = _create_exchange_to_model_schemas(
        schemas_directory, exchange_to_classes_mappings
    )

    # Create head schema, which references all aforementioned schemas. Pydantic
    # v1 does not support creating a single JSON schema for multiple models.

    head_schema = _create_head_schema(schema_files, schemas_directory)

    # Create a single documentation page for all schemas, by referencing the
    # head schema that includes them

    html_file = _create_documentation(head_schema, documentation_directory)

    return html_file, documentation_directory, schemas_directory
