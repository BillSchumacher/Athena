#!/bin/sh

if [ "$ATHENA_MODE" = "api" ]; then
    echo "Running Athena API..."
    exec python -m athena.api
else
    echo "Running Athena in CLI mode..."
    exec python -m athena.__main__
fi