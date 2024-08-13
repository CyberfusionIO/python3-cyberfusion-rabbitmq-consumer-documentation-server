import os
from typing import Tuple

from fastapi.testclient import TestClient

from cyberfusion.RabbitMQConsumerDocumentationServer.fastapi_server import (
    PREFIX_HTML,
    PREFIX_SCHEMAS,
)
from tests._utilities import get_first_file_in_directory


def test_html_root(
    server_test_client: TestClient,
    server_create_documentation_mock: Tuple[str, str, str],
    head_schema_path: str,
    schemas_directory_path: str,
    html_documentation_directory_path: str,
) -> None:
    response = server_test_client.get(PREFIX_HTML)

    assert response.status_code == 200
    assert response.text


def test_html_sub(
    server_test_client: TestClient,
    server_create_documentation_mock: Tuple[str, str, str],
    head_schema_path: str,
    schemas_directory_path: str,
    html_documentation_directory_path: str,
) -> None:
    file_ = get_first_file_in_directory(html_documentation_directory_path)

    url = PREFIX_HTML + "/" + file_

    response = server_test_client.get(url)

    assert response.status_code == 200
    assert response.text


def test_schemas_root(
    server_test_client: TestClient,
    server_create_documentation_mock: Tuple[str, str, str],
    head_schema_path: str,
    schemas_directory_path: str,
    html_documentation_directory_path: str,
) -> None:
    amount_files = os.listdir(schemas_directory_path)

    response = server_test_client.get(PREFIX_SCHEMAS)

    assert response.status_code == 200
    assert response.json() == amount_files


def test_schema_single(
    server_test_client: TestClient,
    server_create_documentation_mock: Tuple[str, str, str],
    head_schema_path: str,
    schemas_directory_path: str,
    html_documentation_directory_path: str,
) -> None:
    file_ = get_first_file_in_directory(schemas_directory_path)

    url = PREFIX_SCHEMAS + "/" + file_

    response = server_test_client.get(url)

    assert response.status_code == 200
    assert response.text
