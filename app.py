from flask import Flask, redirect, url_for, render_template
from flask_pymongo import PyMongo
from flask_login import LoginManager, login_required
from bson.objectid import ObjectId
from models import User
from auth_routes import auth_bp

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/barbershop_db"
app.secret_key = "supersecretkey"

mongo = PyMongo(app)
app.mongo = mongo

def get_mongo():
    return mongo

login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    mongo = get_mongo()
    from bson import ObjectId
    try:
        user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    except Exception:
        return None
    return User(user_data) if user_data else None

app.register_blueprint(auth_bp, url_prefix="/auth")

@app.route("/")
def home():
    return redirect(url_for("auth.login"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)
