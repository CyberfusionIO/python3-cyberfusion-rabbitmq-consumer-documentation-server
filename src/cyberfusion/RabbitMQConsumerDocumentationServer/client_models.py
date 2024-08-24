"""Utilities to create client-side models."""

import os
import subprocess
from pathlib import Path
from typing import List

VERSION_PYTHON = "3.11"


def generate_pydantic_models_from_single_json_schema(
    json_schema_path: str, output_file_path: str
) -> None:
    """Create Pydantic models for single JSON schema."""
    subprocess.check_output(
        [
            "datamodel-codegen",
            "--input-file-type",
            "jsonschema",
            "--input",
            json_schema_path,
            "--output",
            output_file_path,
            "--target-python-version",
            VERSION_PYTHON,
        ]
    )


def generate_pydantic_models_from_multiple_json_schemas(
    json_schemas_paths: List[str], output_directory_path: str
) -> None:
    """Create Pydantic models for multiple JSON schema.

    To the specified output directory, one file per JSON schema will be written.
    The file name is the stem of the schema's basename + `.py`.

    Example:
        JSON schema path: `/tmp/example.json`
        Output path: output_directory_path + `example.py`

    The specified directory must already exist.
    """
    for json_schema_path in json_schemas_paths:
        output_path = (
            os.path.join(
                output_directory_path,
                Path(os.path.basename(json_schema_path)).stem,
            )
            + ".py"
        )

        generate_pydantic_models_from_single_json_schema(json_schema_path, output_path)
