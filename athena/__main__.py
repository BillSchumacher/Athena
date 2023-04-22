from athena.input_processor import process_input
from athena.loguru_config import setup_logging
import os
import click


@click.command()
@click.option(
    "--log-level",
    type=str,
    default=os.getenv("LOG_LEVEL", "INFO"),
    help="Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
)
def main(log_level):
    setup_logging(log_level)
    print("Welcome to Athena!")
    username = input("Please enter your name: ")

    try:
        while True:
            user_input = input(f"{username}: ")
            if user_input.lower() in ["exit", "quit"]:
                break

            response = process_input(user_input, username)
            print(f"Athena: {response}")
    except KeyboardInterrupt:
        pass
    print("Athena: Goodbye!")


if __name__ == "__main__":
    main()
