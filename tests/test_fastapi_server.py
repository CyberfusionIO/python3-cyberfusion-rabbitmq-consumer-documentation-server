import os
from typing import Tuple

from fastapi.testclient import TestClient

from cyberfusion.RabbitMQConsumerDocumentationServer.fastapi_server import (
    PREFIX_HTML,
    PREFIX_SCHEMAS,
)
from tests._utilities import get_first_file_in_directory


def test_html(
    server_test_client: TestClient,
    server_create_documentation_mock: Tuple[str, str, str],
    head_schema: str,
    schemas_directory: str,
    documentation_directory: str,
) -> None:
    response = server_test_client.get(PREFIX_HTML)

    assert response.status_code == 200
    assert response.text


def test_html_subpath(
    server_test_client: TestClient,
    server_create_documentation_mock: Tuple[str, str, str],
    head_schema: str,
    schemas_directory: str,
    documentation_directory: str,
) -> None:
    file_ = get_first_file_in_directory(documentation_directory)

    url = PREFIX_HTML + "/" + file_

    response = server_test_client.get(url)

    assert response.status_code == 200
    assert response.text


def test_schemas(
    server_test_client: TestClient,
    server_create_documentation_mock: Tuple[str, str, str],
    head_schema: str,
    schemas_directory: str,
    documentation_directory: str,
) -> None:
    amount_files = os.listdir(schemas_directory)

    response = server_test_client.get(PREFIX_SCHEMAS)

    assert response.status_code == 200
    assert response.json() == amount_files


def test_schema(
    server_test_client: TestClient,
    server_create_documentation_mock: Tuple[str, str, str],
    head_schema: str,
    schemas_directory: str,
    documentation_directory: str,
) -> None:
    file_ = get_first_file_in_directory(schemas_directory)

    url = PREFIX_SCHEMAS + "/" + file_

    response = server_test_client.get(url)

    assert response.status_code == 200
    assert response.text
