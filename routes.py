from flask import Blueprint, redirect, url_for, request, jsonify, render_template
from app import get_mongo

app_bp = Blueprint('app_bp', __name__)

mongo = get_mongo()

@app_bp.route('/')
def home():
    return redirect(url_for("auth.login"))  # Redirect to login page

@app_bp.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    if request.method == 'POST':
        # Process appointment data here
        data = request.form  # or request.get_json() for JSON
        # Save appointment logic...
        return jsonify({"message": "Appointment added!", "data": data}), 201
    return render_template("add_appointment.html")
