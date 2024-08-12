# python3-cyberfusion-rabbitmq-consumer-documentation-server

Auto-generated documentation server for RPC exchange responses and requests.

![HTML documentation: request](assets/request.png)
*Request*

![HTML documentation: response](assets/response.png)
*Response*

# Install

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

## Start

### Manually

    /usr/bin/rabbitmq-consumer-documentation-server --config-file-path=... --host=:: --port=9012

Set `--config-file-path` to the RabbitMQ consumer config file.

### systemd

    systemctl start rabbitmq-consumer-documentation-server.service

#### Environment variables

* `CONFIG_FILE_PATH` (`--config-file-path`). Default: `/etc/cyberfusion/rabbitmq.yml`
* `HOST` (`--host`). Default: `::`
* `PORT` (`--port`). Default: `9012`

## Web server

On the given host and port, a web server is started. It serves the documentation.

# Tests

Run tests with pytest:

    pytest tests/
