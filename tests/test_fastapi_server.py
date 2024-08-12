from typing import Tuple

from fastapi.testclient import TestClient

from cyberfusion.RabbitMQConsumerDocumentationServer.fastapi_server import (
    PREFIX_HTML,
    PREFIX_SCHEMAS,
)
from tests._utilities import get_first_file_in_directory


def test_root(server_test_client: TestClient) -> None:
    response = server_test_client.get("/", follow_redirects=False)
    assert response.status_code == 308

    response = server_test_client.get(
        response.headers["location"], follow_redirects=False
    )
    assert response.status_code == 200


def test_html(
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
    file_ = get_first_file_in_directory(schemas_directory)

    url = PREFIX_SCHEMAS + "/" + file_

    response = server_test_client.get(url)

    assert response.status_code == 200
    assert response.text
