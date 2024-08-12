"""A setuptools based setup module."""

from setuptools import setup

setup(
    name="python3-cyberfusion-rabbitmq-consumer-documentation-server",
    version="1.0",
    description="Auto-generated documentation server for RPC exchange responses and requests.",
    author="William Edwards",
    author_email="wedwards@cyberfusion.nl",
    url="https://vcs.cyberfusion.nl/core/python3-cyberfusion-rabbitmq-consumer-documentation-server",
    license="Closed",
    packages=[
        "cyberfusion.RabbitMQConsumerDocumentationServer",
    ],
    package_dir={"": "src"},
    platforms=["linux"],
    data_files=[],
    entry_points={
        "console_scripts": [
            "rabbitmq-consumer-documentation-server=cyberfusion.RabbitMQConsumerDocumentationServer.cli:main",
        ]
    },
)
