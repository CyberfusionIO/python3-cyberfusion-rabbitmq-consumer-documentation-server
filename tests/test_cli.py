import docopt
from pytest_mock import MockerFixture

from cyberfusion.RabbitMQConsumerDocumentationServer import cli


def test_cli_run(mocker: MockerFixture) -> None:
    HOST = "::"
    PORT = 9013

    mocker.patch(
        "cyberfusion.RabbitMQConsumerDocumentationServer.cli.get_args",
        return_value=docopt.docopt(
            cli.__doc__,
            [
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
