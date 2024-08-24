import os
from typing import List

from cyberfusion.RabbitMQConsumerDocumentationServer.client_models import (
    generate_pydantic_models_from_multiple_json_schemas,
    generate_pydantic_models_from_single_json_schema,
)
from cyberfusion.RabbitMQConsumerDocumentationServer.utilities import (
    get_tmp_path,
)
from tests._utilities import get_first_file_in_directory


def test_generate_pydantic_models_from_single_json_schema(
    schemas_files_paths: List[str],
) -> None:
    json_schema_path = schemas_files_paths[0]
    output_file_path = get_tmp_path()

    assert not os.path.isfile(output_file_path)

    generate_pydantic_models_from_single_json_schema(json_schema_path, output_file_path)

    assert os.path.isfile(output_file_path)

    with open(output_file_path, "r") as f:
        code = f.read()

    assert "class " in code
    assert "(BaseModel):" in code


def test_generate_pydantic_models_from_multiple_json_schemas(
    schemas_files_paths: List[str],
) -> None:
    output_directory_path = get_tmp_path()

    assert not os.path.isdir(output_directory_path)
    os.mkdir(output_directory_path)

    generate_pydantic_models_from_multiple_json_schemas(
        schemas_files_paths, output_directory_path
    )

    # Test count

    assert len(os.listdir(output_directory_path)) == len(schemas_files_paths)

    # Test code

    with open(
        os.path.join(
            output_directory_path,
            get_first_file_in_directory(output_directory_path),
        ),
        "r",
    ) as f:
        code = f.read()

    assert "class " in code
    assert "(BaseModel):" in code
