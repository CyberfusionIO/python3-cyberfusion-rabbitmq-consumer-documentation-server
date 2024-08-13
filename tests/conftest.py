from typing import List, Tuple

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from cyberfusion.RabbitMQConsumerDocumentationServer.fastapi_server import (
    get_app,
)
from cyberfusion.RabbitMQConsumerDocumentationServer.generator import (
    ExchangeToModelsMapping,
    _create_head_schema,
    _create_html_documentation_directory,
    create_exchange_to_model_schemas,
    create_exchange_to_models_mappings,
    create_schemas_directory,
    generate_html_documentation,
)


@pytest.fixture
def server_app() -> FastAPI:
    return get_app()


@pytest.fixture
def server_test_client(server_app: FastAPI) -> TestClient:
    return TestClient(server_app)


@pytest.fixture
def html_documentation_directory_path() -> str:
    return _create_html_documentation_directory()


@pytest.fixture
def schemas_directory_path() -> str:
    return create_schemas_directory()


@pytest.fixture
def schemas_files_paths(
    schemas_directory_path: str,
    exchange_to_models_mappings: List[ExchangeToModelsMapping],
) -> List[str]:
    return create_exchange_to_model_schemas(
        schemas_directory_path, exchange_to_models_mappings
    )


@pytest.fixture
def exchange_to_models_mappings() -> List[ExchangeToModelsMapping]:
    exchange_to_models_mappings = create_exchange_to_models_mappings()

    # Ensure we're actually testing something

    assert (
        len(exchange_to_models_mappings) >= 1
    ), "No exchanges found. Installed exchanges in editable mode? Our way of discovering exchanges (`cyberfusion.RabbitMQConsumer.utilities.import_installed_handler_modules`) does not support that. Install regularly."

    return exchange_to_models_mappings


@pytest.fixture
def head_schema_path(schemas_files_paths, schemas_directory_path: str) -> str:
    return _create_head_schema(schemas_files_paths, schemas_directory_path)


@pytest.fixture
def server_create_documentation_mock(
    mocker: MockerFixture,
    schemas_directory_path: str,
    html_documentation_directory_path: str,
) -> Tuple[str, str, str]:
    mocker.patch(
        "cyberfusion.RabbitMQConsumerDocumentationServer.generator._create_html_documentation_directory",
        return_value=html_documentation_directory_path,
    )
    mocker.patch(
        "cyberfusion.RabbitMQConsumerDocumentationServer.generator.create_schemas_directory",
        return_value=schemas_directory_path,
    )

    html_file, html_documentation_directory_path, schemas_directory_path = (
        generate_html_documentation()
    )

    mocker.patch(
        "cyberfusion.RabbitMQConsumerDocumentationServer.fastapi_server.generate_html_documentation",
        return_value=(
            html_file,
            html_documentation_directory_path,
            schemas_directory_path,
        ),
    )

    return html_file, html_documentation_directory_path, schemas_directory_path
