from typing import Any

from athena import celery_app


@celery_app.task
def example_task(x, y) -> Any:
    """
    This is an example task that can be called asynchronously from anywhere
        in the codebase.

    Args:
        x (Any): First value
        y (Any): Second value

    Returns:
        Any: The sum of x and y
    """
    return x + y
