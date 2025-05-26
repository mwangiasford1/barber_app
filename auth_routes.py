from flask import Blueprint, request, render_template, redirect, url_for, jsonify, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from bson.objectid import ObjectId

auth_bp = Blueprint("auth", __name__)

def get_mongo():
    return current_app.mongo

@auth_bp.route("/")
def home():
    return redirect(url_for("auth.login"))

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    mongo = get_mongo()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = mongo.db.users.find_one({"username": username})
        if user and check_password_hash(user["password"], password):
            login_user(User(user))
            return redirect(url_for('dashboard'))  # Make sure this route exists in app.py
        else:
            flash("Invalid credentials", "error")
    return render_template("login.html")

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth_bp.route('/admin-dashboard')
@login_required
def admin_dashboard():
    if hasattr(current_user, "is_admin") and current_user.is_admin():
        return jsonify({"message": "Welcome, Admin!"})
    return jsonify({"error": "Access Denied"}), 403

@auth_bp.route('/barber-dashboard')
@login_required
def barber_dashboard():
    if hasattr(current_user, "is_barber") and current_user.is_barber():
        return jsonify({"message": "Welcome, Barber!"})
    return jsonify({"error": "Access Denied"}), 403

@auth_bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if not username or not email or not password:
            flash("All fields are required!", "error")
            return redirect(url_for('auth.register'))
        mongo = get_mongo()
        if mongo.db.users.find_one({"email": email}):
            flash("Email already exists!", "error")
            return redirect(url_for('auth.register'))
        hashed_password = generate_password_hash(password)
        mongo.db.users.insert_one({
            "username": username,
            "email": email,
            "password": hashed_password,
            "role": "customer"
        })
        flash("User created successfully!", "success")
        return redirect(url_for('auth.login'))
    return render_template("register.html")

@auth_bp.route('/add_appointment', methods=['GET', 'POST'])
@login_required
def add_appointment():
    mongo = get_mongo()
    if request.method == 'POST':
        data = request.form
        appointment = {
            "user_id": current_user.id,
            "name": data.get('name', current_user.username),
            "service": data.get('service'),
            "date": data.get('date'),
            "time": data.get('time'),
            "price": data.get('price'),
            "payment_method": data.get('payment_method'),  # Save payment method
            "status": "booked"
        }
        mongo.db.appointments.insert_one(appointment)
        flash("Appointment booked!", "success")
        return redirect(url_for('auth.my_appointments'))
    return render_template("add_appointment.html")

@auth_bp.route('/my_appointments')
@login_required
def my_appointments():
    mongo = get_mongo()
    appointments = list(mongo.db.appointments.find({"user_id": current_user.id}))
    # Convert ObjectId to string for JSON
    for appt in appointments:
        appt['_id'] = str(appt['_id'])
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
        return jsonify({"appointments": appointments})
    return render_template("my_appointments.html", appointments=appointments)

@auth_bp.route('/cancel_appointment/<appointment_id>')
@login_required
def cancel_appointment(appointment_id):
    mongo = get_mongo()
    mongo.db.appointments.delete_one({
        "_id": ObjectId(appointment_id),
        "user_id": current_user.id
    })
    flash("Appointment cancelled.", "success")
    return redirect(url_for('auth.my_appointments'))

@auth_bp.route('/ai_assistant', methods=['GET', 'POST'])
@login_required
def ai_assistant():
    response = None
    if request.method == 'POST':
        user_question = request.form.get('question')
        # Placeholder AI logic (replace with real AI API call)
        if user_question:
            # Example: simple keyword-based response
            if "hours" in user_question.lower():
                response = "We are open from 9am to 7pm, Monday to Saturday."
            elif "services" in user_question.lower():
                response = "We offer haircuts, beard trims, and more. Check our services page!"
            else:
                response = "I'm here to help! Please ask about our services, hours, or appointments."
    return render_template("ai_assistant.html", response=response)
