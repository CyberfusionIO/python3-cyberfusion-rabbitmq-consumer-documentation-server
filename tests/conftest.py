from typing import List, Tuple

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from cyberfusion.RabbitMQConsumerDocumentationServer.fastapi_server import (
    get_app,
)
from cyberfusion.RabbitMQConsumerDocumentationServer.generator import (
    ExchangeToClassesMapping,
    _create_documentation_directory,
    _create_exchange_to_classes_mappings,
    _create_exchange_to_model_schemas,
    _create_head_schema,
    _create_schemas_directory,
    generate_documentation,
)


@pytest.fixture
def server_app() -> FastAPI:
    return get_app()


@pytest.fixture
def server_test_client(server_app: FastAPI) -> TestClient:
    return TestClient(server_app)


@pytest.fixture
def documentation_directory() -> str:
    return _create_documentation_directory()


@pytest.fixture
def schemas_directory() -> str:
    return _create_schemas_directory()


@pytest.fixture
def exchange_to_model_schemas(
    schemas_directory: str,
    exchange_to_classes_mappings: List[ExchangeToClassesMapping],
) -> List[str]:
    return _create_exchange_to_model_schemas(
        schemas_directory, exchange_to_classes_mappings
    )


@pytest.fixture
def exchange_to_classes_mappings() -> List[ExchangeToClassesMapping]:
    exchange_to_classes_mappings = _create_exchange_to_classes_mappings()

    # Ensure we're actually testing something

    assert (
        len(exchange_to_classes_mappings) >= 1
    ), "No exchanges found. Installed exchanges in editable mode? Our way of discovering exchanges (`cyberfusion.RabbitMQConsumer.utilities.import_installed_handler_modules`) does not support that. Install regularly."

    return exchange_to_classes_mappings


@pytest.fixture
def head_schema(
    exchange_to_model_schemas: List[str], schemas_directory: str
) -> str:
    return _create_head_schema(exchange_to_model_schemas, schemas_directory)


@pytest.fixture
def server_create_documentation_mock(
    mocker: MockerFixture,
    schemas_directory: str,
    documentation_directory: str,
) -> Tuple[str, str, str]:
    mocker.patch(
        "cyberfusion.RabbitMQConsumerDocumentationServer.generator._create_documentation_directory",
        return_value=documentation_directory,
    )
    mocker.patch(
        "cyberfusion.RabbitMQConsumerDocumentationServer.generator._create_schemas_directory",
        return_value=schemas_directory,
    )

    html_file, documentation_directory, schemas_directory = (
        generate_documentation()
    )

    mocker.patch(
        "cyberfusion.RabbitMQConsumerDocumentationServer.fastapi_server.generate_documentation",
        return_value=(html_file, documentation_directory, schemas_directory),
    )

    return html_file, documentation_directory, schemas_directory
