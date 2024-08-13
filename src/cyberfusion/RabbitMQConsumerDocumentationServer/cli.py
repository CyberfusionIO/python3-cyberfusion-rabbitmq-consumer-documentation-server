"""Server serving generated documentation using Bottle.

Usage:
  rabbitmq-consumer-documentation-server [--host=<host>] [--port=<port>]

Options:
  -h --help                                      Show this screen.
  --host=<host>                                  Host to listen on. [default: ::]
  --port=<port>                                  Port to listen on. [default: 9012]
"""

import docopt
import uvicorn
from schema import Schema, Use

from cyberfusion.RabbitMQConsumerDocumentationServer.fastapi_server import (
    get_app,
)


def get_args() -> docopt.Dict:  # pragma: no cover
    """Get docopt args."""
    return docopt.docopt(__doc__)


def main() -> None:
    """Start Uvicorn, serving FastAPI app."""
    args = get_args()
    schema = Schema({"--host": str, "--port": Use(int)})
    args = schema.validate(args)

    app = get_app()

    uvicorn.run(
        app,
        host=args["--host"],
        port=args["--port"],
        log_level="info",
    )
