"""FastAPI-based server, serving documentation and schemas."""

import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from cyberfusion.RabbitMQConsumerDocumentationServer.generator import (
    generate_html_documentation,
)

PREFIX_SCHEMAS = "/schemas"


def get_app() -> FastAPI:
    """Get FastAPI app."""
    html_file_path, html_documentation_directory, schemas_directory = (
        generate_html_documentation()
    )

    app = FastAPI(
        title="RabbitMQ Consumer Documentation Server",
        docs_url=None,
        redoc_url=None,
    )

    @app.get("/")  # type: ignore[misc]
    def show_html_documentation() -> HTMLResponse:
        """Show HTML documentation."""
        return HTMLResponse(
            open(
                os.path.join(html_documentation_directory, html_file_path), "r"
            ).read()
        )

    @app.get(PREFIX_SCHEMAS)  # type: ignore[misc]
    def list_schemas() -> JSONResponse:
        """List schemas."""
        return JSONResponse(os.listdir(schemas_directory))

    app.mount(
        PREFIX_SCHEMAS, StaticFiles(directory=schemas_directory, html=True)
    )
    app.mount(  # Serve `js` + `css` + `font`
        "/",
        StaticFiles(directory=html_documentation_directory, html=True),
    )

    return app
