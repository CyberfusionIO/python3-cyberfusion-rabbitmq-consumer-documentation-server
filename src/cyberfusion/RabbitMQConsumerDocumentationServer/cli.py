"""Server serving generated documentation using Bottle.

Usage:
  rabbitmq-consumer-documentation-server --config-file-path=<config-file-path> [--host=<host>] [--port=<port>]

Options:
  -h --help                                      Show this screen.
  --config-file-path=<config-file-path>          Path to config file.
  --host=<host>                                  Host to listen on. [default: ::]
  --port=<port>                                  Port to listen on. [default: 9012]
"""

import docopt
import uvicorn
from schema import Schema, Use

from cyberfusion.RabbitMQConsumer.config import Config
from cyberfusion.RabbitMQConsumerDocumentationServer.fastapi_server import (
    get_app,
)


def get_args() -> docopt.Dict:
    """Get docopt args."""
    return docopt.docopt(__doc__)


def main() -> None:
    """Start Uvicorn, serving FastAPI app."""
    args = get_args()
    schema = Schema(
        {"--config-file-path": str, "--host": str, "--port": Use(int)}
    )
    args = schema.validate(args)

    config = Config(args["--config-file-path"])

    app = get_app(config)

    uvicorn.run(
        app,
        host=args["--host"],
        port=args["--port"],
        log_level="info",
    )
