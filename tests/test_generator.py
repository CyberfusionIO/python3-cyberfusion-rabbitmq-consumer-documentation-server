import json
import os
from typing import List

from cyberfusion.RabbitMQConsumer.contracts import RPCResponseBase
from cyberfusion.RabbitMQConsumerDocumentationServer import generator
from cyberfusion.RabbitMQConsumerDocumentationServer.generator import (
    KEY_EXAMPLES,
    ExchangeToModelsMapping,
    _create_head_schema,
    _create_html_documentation,
    _create_html_documentation_directory,
    _inject_default_examples,
    create_exchange_to_model_schemas,
    create_schemas_directory,
)
from cyberfusion.RabbitMQHandlers.exchanges.dx_example import (
    RPCResponseExample,
)


def test_generate_html_documentation() -> None:
    html_file, html_documentation_directory_path, schemas_directory_path = (
        generator.generate_html_documentation()
    )

    assert os.path.isdir(html_documentation_directory_path)
    assert os.path.isfile(
        os.path.join(html_documentation_directory_path, html_file)
    )

    assert os.path.isdir(schemas_directory_path)


def test_create_schemas_directory() -> None:
    assert os.path.isdir(create_schemas_directory())


def test_create_html_documentation_directory() -> None:
    assert os.path.isdir(_create_html_documentation_directory())


def test_inject_default_examples_absent() -> None:
    assert KEY_EXAMPLES not in RPCResponseBase.Config.schema_extra

    response = _inject_default_examples(RPCResponseBase)

    assert KEY_EXAMPLES in response.Config.schema_extra


def test_inject_default_examples_present() -> None:
    assert KEY_EXAMPLES in RPCResponseExample.Config.schema_extra

    ORIGINAL_COUNT = len(RPCResponseExample.Config.schema_extra[KEY_EXAMPLES])

    response = _inject_default_examples(RPCResponseExample)

    assert (
        len(response.Config.schema_extra[KEY_EXAMPLES]) == ORIGINAL_COUNT + 1
    )


def test_create_exchange_to_model_schemas(
    schemas_directory_path: str,
    exchange_to_models_mappings: List[ExchangeToModelsMapping],
) -> None:
    schemas_files_paths = create_exchange_to_model_schemas(
        schemas_directory_path, exchange_to_models_mappings
    )

    assert len(schemas_files_paths) == len(exchange_to_models_mappings)

    for idx, schema_file_path in enumerate(schemas_files_paths):
        with open(schema_file_path, "r") as f:
            schema = json.loads(f.read())

        assert (
            schema["title"] == exchange_to_models_mappings[idx].exchange_name
        )
        assert schema["type"] == "object"
        assert schema["properties"] == {
            "request_model": {
                "$ref": "#/definitions/"
                + exchange_to_models_mappings[idx].request_model.__name__
            },
            "response_model": {
                "$ref": "#/definitions/"
                + exchange_to_models_mappings[idx].response_model.__name__
            },
        }
        assert schema["required"] == ["request_model", "response_model"]
        assert (
            exchange_to_models_mappings[idx].request_model.__name__
            in schema["definitions"]
        )
        assert (
            exchange_to_models_mappings[idx].response_model.__name__
            in schema["definitions"]
        )


def test_create_head_schema(
    schemas_directory_path: str, schemas_files_paths: List[str]
) -> None:
    head_schema_path = _create_head_schema(
        schemas_files_paths, schemas_directory_path
    )

    with open(head_schema_path, "r") as f:
        head_schema = json.loads(f.read())

    assert "allOf" in head_schema

    for schema_file_path in schemas_files_paths:
        assert {"$ref": schema_file_path} in head_schema["allOf"]


def test_create_documentation(
    head_schema_path: str, schemas_directory_path: str
) -> None:
    html_file_path = _create_html_documentation(
        head_schema_path, schemas_directory_path
    )

    assert os.path.isfile(os.path.join(schemas_directory_path, html_file_path))
