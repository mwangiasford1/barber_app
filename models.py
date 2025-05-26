from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# User Model
class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data.get("_id"))
        self.username = user_data.get("username")
        self.email = user_data.get("email")
        self.password = user_data.get("password")
        self.role = user_data.get("role", "customer")  # Default to customer

    def is_admin(self):
        return self.role == "admin"

    def is_barber(self):
        return self.role == "barber"

    def check_password(self, password):
        return check_password_hash(self.password, password)


