# python3-cyberfusion-rabbitmq-consumer-documentation-server

Documentation server for [RabbitMQ consumer](https://github.com/CyberfusionIO/python3-cyberfusion-rabbitmq-consumer) (lean RPC framework).

Features:

* Human-readable HTML documentation.
* [JSON schemas](https://json-schema.org/) for exchange response/request models.
* [Pydantic](https://docs.pydantic.dev/latest/) model generation for exchange request/request models (*definitions*).
* * This allows for strong-contracted bidirectional communication (identical, enforced models on server and client), similar to the intent of [protobuf](https://protobuf.dev/).

## HTML documentation

URL: `/`

![HTML documentation: request](assets/request.png)
*Request*

![HTML documentation: response](assets/response.png)
*Response*

## JSON schemas

URL: `/schemas`

The root returns a list of schemas. Every schema can be accessed as a subpath. For example: `/schemas/dx_example.json`

The list always includes a schema called `head.json`. This schema includes all schemas.

## Pydantic model generation

Automatically generate [Pydantic](https://docs.pydantic.dev/latest/) for request/response models of all installed exchanges.

One Python file (containing Pydantic models) is written per exchange, in a single directory (which is output to stdout).

Example:

```bash
$ rabbitmq-consumer-documentation-server create-client-models
/tmp/ce2e67f5-b756-4526-a4ac-45008d6f6526

$ ls -l /tmp/ce2e67f5-b756-4526-a4ac-45008d6f6526
total 24
-rw-r--r--  1 example  example  1024 Aug 13 15:16 dx_example.py
```

Example Python file (`dx_example.py`):

```python
# generated by datamodel-codegen:
#   filename:  dx_example.json
#   timestamp: 2024-08-13T13:16:16+00:00

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class FavouriteFoodEnum(Enum):
    onion = 'onion'
    orange = 'orange'
    banana = 'banana'


class RPCRequestExample(BaseModel):
    favourite_food: FavouriteFoodEnum = Field(
        ..., description='Human-readable favourite food.'
    )
    chance_percentage: Optional[PositiveInt] = Field(
        20, description='Chances of favourite food passing.', title='Chance Percentage'
    )


class RPCResponseDataExample(BaseModel):
    tolerable: bool = Field(..., title='Tolerable')


class RPCResponseExample(BaseModel):
    success: bool = Field(..., title='Success')
    message: str = Field(..., title='Message')
    data: Optional[RPCResponseDataExample] = None


class DxExample(BaseModel):
    request_model: RPCRequestExample
    response_model: RPCResponseExample
```

# Install

## PyPI

Run the following command to install the package from PyPI:

    pip3 install python3-cyberfusion-rabbitmq-consumer-documentation-server

## Generic

Run the following command to create a source distribution:

    python3 setup.py sdist

## Debian

Run the following commands to build a Debian package:

    mk-build-deps -i -t 'apt -o Debug::pkgProblemResolver=yes --no-install-recommends -y'
    dpkg-buildpackage -us -uc

# Configure

No configuration is supported.

# Usage

## Start server (serve HTML documentation + JSON schemas)

### Manually

    /usr/bin/rabbitmq-consumer-documentation-server run-server --host=:: --port=9012

### systemd

    systemctl start rabbitmq-consumer-documentation-server.service

## Generate Pydantic models

See '[Pydantic model generation](#pydantic-model-generation)'.

#### Environment variables

* `HOST` (`--host`). Default: `::`
* `PORT` (`--port`). Default: `9012`

# Tests

Run tests with pytest:

    pytest tests/
