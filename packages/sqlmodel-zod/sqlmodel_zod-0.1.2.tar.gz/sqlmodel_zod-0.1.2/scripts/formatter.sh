#!/bin/sh -e
set -x

pip install -r requirements.txt
ruff check sqlmodel_zod --fix
ruff format sqlmodel_zod