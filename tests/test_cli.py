import os

import docopt
from _pytest.capture import CaptureFixture
from pytest_mock import MockerFixture

from cyberfusion.RabbitMQConsumerDocumentationServer import cli


def test_create_client_models(
    mocker: MockerFixture, capsys: CaptureFixture
) -> None:
    mocker.patch(
        "cyberfusion.RabbitMQConsumerDocumentationServer.cli.get_args",
        return_value=docopt.docopt(
            cli.__doc__,
            ["create-client-models"],
        ),
    )

    cli.main()

    output = capsys.readouterr().out.splitlines()

    directory = output[0]

    assert os.path.isdir(directory)
    assert os.listdir(directory)


def test_cli_run_server(mocker: MockerFixture) -> None:
    HOST = "::"
    PORT = 9013

    mocker.patch(
        "cyberfusion.RabbitMQConsumerDocumentationServer.cli.get_args",
        return_value=docopt.docopt(
            cli.__doc__,
            [
                "run-server",
                "--host",
                "::",
                "--port",
                PORT,
            ],
        ),
    )

    uvicorn_mock = mocker.patch("uvicorn.run")

    cli.main()

    uvicorn_mock.assert_called_once_with(
        mocker.ANY, host=HOST, port=PORT, log_level="info"
    )
