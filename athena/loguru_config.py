def setup_logging(logging_level):
    import sys

    from loguru import logger

    logger.remove()
    logger.add(sys.stderr, level=logging_level)
    logger.info(
        f"Logging is configured for {logging_level} level."
    )  # Adjust the level to "DEBUG", "WARNING", "ERROR", or "CRITICAL" as needed
