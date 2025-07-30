#!/bin/bash

# main CI script. Run in a docker container, locally or in github actions
# assuming all dependencies are installed

set -e

ruff check src tests
mypy src
pytest --cov=src --cov-report term-missing tests
