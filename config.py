import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
    MONGO_URI = "mongodb://localhost:27017/barbershop_db"
