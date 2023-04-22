from athena.plugins.plugin_base import PluginBase


class AuthenticationPlugin(PluginBase):
    def __init__(self, user_manager):
        super().__init__("Authentication", "Handles user authentication and registration.")
        self.user_manager = user_manager

    def can_process(self, input_text):
        return any(keyword in input_text.lower() for keyword in ["register", "authenticate", "login", "sign up"])

    def process(self, input_text):
        input_text = input_text.lower().strip()
        words = input_text.split()
        if len(words) != 3:
            return "Please provide your username and password."

        command, username, password = words
        if command in ["register", "sign up"]:
            if self.user_manager.register_user(username, password):
                return f"User {username} registered successfully."
            else:
                return f"User {username} already exists."
        elif command in ["authenticate", "login"]:
            if self.user_manager.authenticate_user(username, password):
                return f"User {username} authenticated successfully."
            else:
                return "Invalid username or password."
        else:
            return "Invalid command. Please use 'register' or 'authenticate'."
