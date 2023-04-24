from loguru import logger


class UserManager:
    def __init__(self):
        logger.debug("Initializing user manager...")
        self.users = {}

    def register_user(self, username, password):
        logger.debug(f"Registering user {username}...")
        if username in self.users:
            logger.debug(f"User {username} already exists.")
            return False
        self.users[username] = {"password": password, "preferences": {}}
        logger.debug(f"User {username} registered successfully.")
        return True

    def authenticate_user(self, username, password):
        logger.debug(f"Authenticating user {username}...")
        success = (
            username in self.users and self.users[username]["password"] == password
        )
        if success:
            logger.debug(f"User {username} authenticated successfully.")
        else:
            logger.debug("Invalid username or password.")
        return success

    def set_user_preference(self, username, key, value):
        logger.debug(f"Setting user preference {key} to {value} for user {username}...")
        if username in self.users:
            self.users[username]["preferences"][key] = value
            logger.debug(f"User preference {key} set successfully.")
            return True
        logger.debug(f"User {username} does not exist.")
        return False

    def get_user_preference(self, username, key):
        logger.debug(f"Getting user preference {key} for user {username}...")
        if username in self.users and key in self.users[username]["preferences"]:
            logger.debug(
                f"User preference {key} found: {self.users[username]['preferences'][key]}"
            )
            return self.users[username]["preferences"][key]
        logger.debug(f"User preference {key} not found.")
        return None
