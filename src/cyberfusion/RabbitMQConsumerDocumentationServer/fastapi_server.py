"""FastAPI-based server, serving documentation and schemas."""

from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from cyberfusion.RabbitMQConsumer.config import Config
from cyberfusion.RabbitMQConsumerDocumentationServer.generator import (
    generate_documentation,
)

PREFIX_HTML = "/html"
PREFIX_SCHEMAS = "/schemas"


def get_app(config: Config) -> FastAPI:
    """Get FastAPI app."""
    html_file, documentation_directory, schemas_directory = (
        generate_documentation(config)
    )

    app = FastAPI(
        title="RabbitMQ Consumer Documentation Server",
        docs_url=None,
        redoc_url=None,
    )

    @app.get("/")  # type: ignore[misc]
    def root() -> RedirectResponse:
        """Redirect from / to HTML documentation."""
        return RedirectResponse(
            f"{PREFIX_HTML}/{html_file}",
            status_code=HTTPStatus.PERMANENT_REDIRECT,
        )

    app.mount(
        PREFIX_HTML, StaticFiles(directory=documentation_directory, html=True)
    )
    app.mount(
        PREFIX_SCHEMAS, StaticFiles(directory=schemas_directory, html=True)
    )

    return app
