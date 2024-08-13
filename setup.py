"""A setuptools based setup module."""

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="python3-cyberfusion-rabbitmq-consumer-documentation-server",
    version="1.1.1",
    description="Auto-generated documentation server for RPC exchange responses and requests.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.11",
    author="William Edwards",
    author_email="wedwards@cyberfusion.nl",
    url="https://vcs.cyberfusion.nl/core/python3-cyberfusion-rabbitmq-consumer-documentation-server",
    packages=[
        "cyberfusion.RabbitMQConsumerDocumentationServer",
    ],
    package_dir={"": "src"},
    platforms=["linux"],
    data_files=[],
    install_requires=[
        "docopt==0.6.2",
        "fastapi==0.92.0",
        "pydantic==1.10.4",
        "schema==0.7.5",
        "uvicorn==0.17.6",
        "json-schema-for-humans==1.0.2",
        "datamodel-code-generator==0.25.9",
    ],
    entry_points={
        "console_scripts": [
            "rabbitmq-consumer-documentation-server=cyberfusion.RabbitMQConsumerDocumentationServer.cli:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=["cyberfusion", "rabbitmq", "amqp", "rpc"],
    license="MIT",
)
