#!/bin/sh

if [ "$ATHENA_MODE" = "api" ]; then
    echo "Running Athena API..."
    exec python -m athena.api
elif [ "$ATHENA_MODE" = "test" ]; then
    echo "Running Athena tests..."
    exec pytest .
else
    echo "Running Athena in CLI mode..."
    exec python -m athena.__main__
fi
