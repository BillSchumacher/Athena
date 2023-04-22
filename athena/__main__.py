from athena import process_input, UserManager
from athena.plugins.authentication_plugin import AuthenticationPlugin


def main():
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
