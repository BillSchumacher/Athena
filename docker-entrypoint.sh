#!/bin/sh

if [ "$ATHENA_MODE" = "api" ]; then
    echo "Running Athena API..."
    exec python -m athena.api
elif [ "$ATHENA_MODE" = "test" ]; then
    echo "Running Athena tests..."
    exec pytest .
elif [ "$ATHENA_MODE" = "celery_beat" ]; then
    echo "Running Athena Celery Beat..."
    exec celery -A athena beat --loglevel=info
elif [ "$ATHENA_MODE" = "celery" ]; then
    echo "Running Athena Celery..."
    exec celery -A athena worker --loglevel=info
else
    echo "Running Athena in CLI mode..."
    exec python -m athena.__main__
fi
