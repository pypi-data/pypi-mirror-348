# dbridge

[![actions status](https://img.shields.io/github/actions/workflow/status/e3oroush/dbridge/publish-pypi.yml?logo=github&style=)](https://github.com/e3oroush/dbridge/actions)
[![PyPI - Version](https://img.shields.io/pypi/v/dbridge.svg)](https://pypi.org/project/dbridge)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dbridge.svg)](https://pypi.org/project/dbridge)

---

A unified database management server that acts as a bridge between client applications and various database engines, providing a consistent interface for database operations and schema exploration.

This project is a server application that tries to serve all the requriments for any UI applications similar to [dbeaver](https://dbeaver.io/) that can be as a UI database client.

## Table of Contents

## Table of Contents

- [Installation](#installation)
- [Run the Server](#run-the-server)
- [License](#license)

## Installation

```console
pip install dbridge
```

## Run the server

```console
pythom -m dbridge.server.app
```

## DB Connection

A Database connection accepts a custom connection config which depending on the db driver, you are flexible to use any form of config.

## Features

- Supported DBs:
  - sqlite
  - duckdb
  - mysql
  - postgres
  - snowflake
- Get databases
- Get Schemas
- Get tables
- Get columns
- Run a sql file with multiple statements

## TODOs

- [x] Autocomplete and suggestion
- [ ] Edit tables and schemas

## UIs

Here is a list of UI clients that are using this server to provide a dbridge user interface.

- [dbridge.nvim](https://github.com/e3oroush/dbridge.nvim) a neovim plugin
- [dbridge.tui](https://github.com/e3oroush/dbridge.nvim) a terminal user interface developed with [Textual](https://textual.textualize.io/)

## License

`dbridge` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
