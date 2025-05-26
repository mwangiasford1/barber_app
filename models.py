from extensions import db
from werkzeug.security import check_password_hash
from flask_login import UserMixin   # <-- Add this import

class User(UserMixin, db.Model):    # <-- Inherit from UserMixin
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='customer')

    def is_barber(self):
        return self.role == "barber"

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    def get_id(self):
        return str(self.id)

class Appointment(db.Model):
    __tablename__ = 'appointment'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(150))
    service = db.Column(db.String(100))
    date = db.Column(db.String(20))
    time = db.Column(db.String(20))
    price = db.Column(db.String(20))
    payment_method = db.Column(db.String(50))
    status = db.Column(db.String(50))
    paid = db.Column(db.Boolean, default=False)


