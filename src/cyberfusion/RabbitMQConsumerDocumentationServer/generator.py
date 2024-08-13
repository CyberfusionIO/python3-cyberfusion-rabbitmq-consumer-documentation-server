"""Generator.

This module provides all facilities to create documentation.
"""

import json
import os
import subprocess
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
from cyberfusion.RabbitMQConsumerDocumentationServer.utilities import (
    get_tmp_path,
)

KEY_EXAMPLES = "examples"
NAME_SCHEMA_HEAD = "head"


@dataclass
class ExchangeToModelsMapping:
    """Mapping from specific exchange to its request and response models."""

    exchange_name: str
    request_model: RPCRequestBase
    response_model: RPCResponseBase


def create_schemas_directory() -> str:
    """Create directory which contains JSON schemas."""
    path = get_tmp_path()

    os.mkdir(path)

    return path


def _create_html_documentation_directory() -> str:
    """Create directory which contains HTML documentation (based on JSON schemas)."""
    path = get_tmp_path()

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


def create_exchange_to_models_mappings() -> List[ExchangeToModelsMapping]:
    """Map all exchanges to their request and response models."""
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
            ExchangeToModelsMapping(
                exchange_name=module.__name__,
                request_model=request_model,
                response_model=response_model,
            )
        )

    return mappings


def create_exchange_to_model_schemas(
    schemas_directory_path: str,
    exchange_to_models_mappings: List[ExchangeToModelsMapping],
) -> List[str]:
    """Create exchange to model mapping (which request/response models belong to which exchange)."""
    mapping_models = []
    schemas_files_paths = []

    # Construct mapping models

    for mapping in exchange_to_models_mappings:
        model = create_model(
            mapping.exchange_name,
            request_model=(mapping.request_model, ...),
            response_model=(mapping.response_model, ...),
        )

        mapping_models.append(model)

    # Write schemas of models to files

    for model in mapping_models:
        schema_file_path = (
            os.path.join(schemas_directory_path, model.__name__) + ".json"
        )

        with open(schema_file_path, "w") as f:
            json_schema = model.schema_json()

            f.write(json_schema)

        schemas_files_paths.append(schema_file_path)

    return schemas_files_paths


def _create_head_schema(
    schemas_files_paths: List[str], schemas_directory_path: str
) -> str:
    """Create head schema.

    This schema contains references to all JSON schemas, thereby including all
    JSON schemas without the need to merge them.
    """

    # Construct head schema

    head_schema: Dict[str, List[Dict[str, str]]] = {"allOf": []}

    for schema_file_path in schemas_files_paths:
        head_schema["allOf"].append({"$ref": schema_file_path})

    # Write head schema

    head_schema_path = os.path.join(
        schemas_directory_path, NAME_SCHEMA_HEAD + ".json"
    )

    with open(head_schema_path, "w") as f:
        f.write(json.dumps(head_schema))

    return head_schema_path


def _create_html_documentation(
    schema: str, schemas_directory_path: str
) -> str:
    """Create HTML documentation (HTML based on JSON schemas)."""

    # json-schema-for-humans provides a Python API, but not for creating
    # documentation for multiple schemas, while the CLI does. The methods
    # that the CLI uses are not private, but not documented either, so
    # using the CLI is a more stable option.

    subprocess.check_output(
        [
            "generate-schema-doc",
            "--config",
            "template_name=js_offline",
            "--config",
            "with_footer=false",
            schema,
            schemas_directory_path,
        ]
    )

    return Path(schema).stem + ".html"


def generate_html_documentation() -> Tuple[str, str, str]:
    """Generate HTML documentation for exchanges' request and response models."""
    schemas_directory_path = create_schemas_directory()
    html_documentation_directory_path = _create_html_documentation_directory()

    # For every exchange, create schemas for its request and response models

    exchange_to_models_mappings = create_exchange_to_models_mappings()
    schemas_files_paths = create_exchange_to_model_schemas(
        schemas_directory_path, exchange_to_models_mappings
    )

    # Create head schema, which references all aforementioned schemas. Pydantic
    # v1 does not support creating a single JSON schema for multiple models.

    head_schema_path = _create_head_schema(
        schemas_files_paths, schemas_directory_path
    )

    # Create a single documentation page for all schemas, by referencing the
    # head schema that includes them

    html_file_path = _create_html_documentation(
        head_schema_path, html_documentation_directory_path
    )

    return (
        html_file_path,
        html_documentation_directory_path,
        schemas_directory_path,
    )
