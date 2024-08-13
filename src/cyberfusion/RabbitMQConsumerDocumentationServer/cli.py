"""Server serving generated documentation using Bottle.

Usage:
  rabbitmq-consumer-documentation-server run-server [--host=<host>] [--port=<port>]
  rabbitmq-consumer-documentation-server create-client-models

Options:
  -h --help                                      Show this screen.
  --host=<host>                                  Host to listen on. [default: ::]
  --port=<port>                                  Port to listen on. [default: 9012]
"""

import os

import docopt
import uvicorn
from schema import Schema, Use

from cyberfusion.RabbitMQConsumerDocumentationServer.client_models import (
    generate_pydantic_models_from_multiple_json_schemas,
)
from cyberfusion.RabbitMQConsumerDocumentationServer.fastapi_server import (
    get_app,
)
from cyberfusion.RabbitMQConsumerDocumentationServer.generator import (
    create_exchange_to_model_schemas,
    create_exchange_to_models_mappings,
    create_schemas_directory,
)
from cyberfusion.RabbitMQConsumerDocumentationServer.utilities import (
    get_tmp_path,
)


def get_args() -> docopt.Dict:  # pragma: no cover
    """Get docopt args."""
    return docopt.docopt(__doc__)


def main() -> None:
    """Start Uvicorn, serving FastAPI app."""
    args = get_args()
    schema = Schema(
        {
            "run-server": bool,
            "create-client-models": bool,
            "--host": str,
            "--port": Use(int),
        }
    )
    args = schema.validate(args)

    app = get_app()

    if args["create-client-models"]:
        output_directory_path = get_tmp_path()
        schemas_directory_path = create_schemas_directory()
        exchange_to_models_mappings = create_exchange_to_models_mappings()
        schemas_files_paths = create_exchange_to_model_schemas(
            schemas_directory_path, exchange_to_models_mappings
        )

        os.mkdir(output_directory_path)

        generate_pydantic_models_from_multiple_json_schemas(
            schemas_files_paths, output_directory_path
        )

        print(output_directory_path)
    else:
        uvicorn.run(
            app,
            host=args["--host"],
            port=args["--port"],
            log_level="info",
        )
