from loguru import logger

from athena.plugins.plugin_base import PluginBase
from athena.user_manager import UserManager


class AuthenticationPlugin(PluginBase):
    def __init__(self, user_manager: UserManager):
        logger.debug("Initializing authentication plugin...")
        super().__init__(
            "Authentication", "Handles user authentication and registration."
        )
        self.user_manager = user_manager

    def can_process(self, input_text):
        return any(
            keyword in input_text.lower()
            for keyword in ["register", "authenticate", "login", "sign up"]
        )

    def process(self, input_text):
        logger.debug("Auth - Processing input text...")
        input_text = input_text.lower().strip()
        words = input_text.split()
        if len(words) != 3:
            logger.debug(
                "Auth - Invalid command. Please provide your username and password."
            )
            return "Please provide your username and password."

        command, username, password = words
        if command in ["register", "sign up"]:
            logger.debug(f"Auth - Registering user {username}...")
            if self.user_manager.register_user(username, password):
                return f"User {username} registered successfully."
            else:
                return f"User {username} already exists."
        elif command in ["authenticate", "login"]:
            logger.debug(f"Auth - Authenticating user {username}...")
            if self.user_manager.authenticate_user(username, password):
                return f"User {username} authenticated successfully."
            else:
                return "Invalid username or password."
        else:
            logger.debug(
                "Auth - Invalid command. Please use 'register' or 'authenticate'."
            )
            return "Invalid command. Please use 'register' or 'authenticate'."
