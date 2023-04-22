def process_input(user_input):
    # Process the user input and generate a response
    response = "You said: " + user_input
    return response


def main():
    print("Welcome to Athena, the AI Agent. Type 'exit' to end the conversation.")

    while True:
        user_input = input("User: ")

        if user_input.lower() == 'exit':
            print("Athena: Goodbye!")
            break

        response = process_input(user_input)
        print("Athena:", response)


if __name__ == "__main__":
    main()
