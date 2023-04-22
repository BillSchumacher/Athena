class UserManager:
    def __init__(self):
        self.users = {}

    def register_user(self, username, password):
        if username in self.users:
            return False
        self.users[username] = {
            "password": password,
            "preferences": {}
        }
        return True

    def authenticate_user(self, username, password):
        return username in self.users and self.users[username]["password"] == password

    def set_user_preference(self, username, key, value):
        if username in self.users:
            self.users[username]["preferences"][key] = value
            return True
        return False

    def get_user_preference(self, username, key):
        if username in self.users and key in self.users[username]["preferences"]:
            return self.users[username]["preferences"][key]
        return None
