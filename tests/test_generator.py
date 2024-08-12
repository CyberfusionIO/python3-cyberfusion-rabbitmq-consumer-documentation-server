import json
import os
from typing import List

from cyberfusion.RabbitMQConsumer.config import Config
from cyberfusion.RabbitMQConsumer.contracts import RPCResponseBase
from cyberfusion.RabbitMQConsumerDocumentationServer import generator
from cyberfusion.RabbitMQConsumerDocumentationServer.generator import (
    KEY_EXAMPLES,
    ExchangeToClassesMapping,
    _create_documentation,
    _create_documentation_directory,
    _create_exchange_to_model_schemas,
    _create_head_schema,
    _create_schemas_directory,
    _inject_default_examples,
)
from cyberfusion.RabbitMQHandlers.exchanges.dx_example import (
    RPCResponseExample,
)


def test_generate_documentation(rabbitmq_config: Config) -> None:
    html_file, documentation_directory, schemas_directory = (
        generator.generate_documentation(rabbitmq_config)
    )

    assert os.path.isdir(documentation_directory)
    assert os.path.isfile(os.path.join(documentation_directory, html_file))

    assert os.path.isdir(schemas_directory)


def test_create_schemas_directory() -> None:
    assert os.path.isdir(_create_schemas_directory())


def test_create_documentation_directory() -> None:
    assert os.path.isdir(_create_documentation_directory())


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
    schemas_directory: str,
    exchange_to_classes_mappings: List[ExchangeToClassesMapping],
) -> None:
    schema_files = _create_exchange_to_model_schemas(
        schemas_directory, exchange_to_classes_mappings
    )

    assert len(schema_files) == len(exchange_to_classes_mappings)

    for idx, schema_file in enumerate(schema_files):
        with open(schema_file, "r") as f:
            schema = json.loads(f.read())

        assert (
            schema["title"] == exchange_to_classes_mappings[idx].exchange_name
        )
        assert schema["type"] == "object"
        assert schema["properties"] == {
            "request_class": {
                "$ref": "#/definitions/"
                + exchange_to_classes_mappings[idx].request_class.__name__
            },
            "response_class": {
                "$ref": "#/definitions/"
                + exchange_to_classes_mappings[idx].response_class.__name__
            },
        }
        assert schema["required"] == ["request_class", "response_class"]
        assert (
            exchange_to_classes_mappings[idx].request_class.__name__
            in schema["definitions"]
        )
        assert (
            exchange_to_classes_mappings[idx].response_class.__name__
            in schema["definitions"]
        )


def test_create_head_schema(
    schemas_directory: str, exchange_to_model_schemas: List[str]
) -> None:
    schema_file = _create_head_schema(
        exchange_to_model_schemas, schemas_directory
    )

    with open(schema_file, "r") as f:
        head_schema = json.loads(f.read())

    assert "allOf" in head_schema

    for exchange_to_model_schema in exchange_to_model_schemas:
        assert {"$ref": exchange_to_model_schema} in head_schema["allOf"]


def test_create_documentation(
    head_schema: str, schemas_directory: str
) -> None:
    html_file = _create_documentation(head_schema, schemas_directory)

    assert os.path.isfile(os.path.join(schemas_directory, html_file))
