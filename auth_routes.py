from flask import Blueprint, request, render_template, redirect, url_for, jsonify, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Appointment
from extensions import db
import openai

auth_bp = Blueprint("auth", __name__)

# Make sure to set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

@auth_bp.route("/")
def home():
    return redirect(url_for("auth.login"))

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth_bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash("User created successfully!", "success")
        return redirect(url_for('auth.login'))
    return render_template("register.html")

@auth_bp.route('/add_appointment', methods=['GET', 'POST'])
@login_required
def add_appointment():
    if request.method == 'POST':
        date = request.form.get('date')
        time = request.form.get('time')
        service = request.form.get('service')
        price = request.form.get('price')
        # Add any other fields you need

        appointment = Appointment(
            user_id=current_user.id,
            date=date,
            time=time,
            service=service,
            price=price
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Appointment booked! Please proceed to payment.', 'success')
        return redirect(url_for('auth.my_appointments'))  # or url_for('auth.add_appointment') if you want to stay on the booking page

    appointments = Appointment.query.filter_by(user_id=current_user.id).all()
    return render_template('appointments.html', appointments=appointments)

@auth_bp.route('/my_appointments')
@login_required
def my_appointments():
    appointments = Appointment.query.filter_by(user_id=current_user.id).all()
    return render_template("my_appointments.html", appointments=appointments)

@auth_bp.route('/cancel_appointment/<int:appointment_id>')
@login_required
def cancel_appointment(appointment_id):
    appointment = Appointment.query.filter_by(id=appointment_id, user_id=current_user.id).first()
    if appointment:
        db.session.delete(appointment)
        db.session.commit()
        flash("Appointment cancelled.", "success")
    else:
        flash("Appointment not found.", "error")
    return redirect(url_for('auth.my_appointments'))

@auth_bp.route('/ai_assistant', methods=['GET', 'POST'])
@login_required
def ai_assistant():
    response = None
    if request.method == 'POST':
        user_question = request.form.get('question')
        if user_question:
            try:
                ai_result = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant for a barbershop."},
                        {"role": "user", "content": user_question}
                    ]
                )
                response = ai_result['choices'][0]['message']['content']
            except Exception:
                response = "Sorry, I couldn't process your request right now."
    return render_template("ai_assistant.html", response=response)

@auth_bp.route('/pay/<int:appointment_id>', methods=['GET', 'POST'])
@login_required
def pay(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    if request.method == 'POST':
        payment_method = request.form.get('payment_method')
        # You can process each payment method as needed
        if payment_method == 'credit_card':
            card_number = request.form.get('card_number')
            expiry = request.form.get('expiry')
            cvv = request.form.get('cvv')
            # Add your credit card processing logic here
        elif payment_method == 'bank_transfer':
            bank_name = request.form.get('bank_name')
            account_number = request.form.get('account_number')
            # Add your bank transfer processing logic here
        elif payment_method == 'paypal':
            paypal_email = request.form.get('paypal_email')
            # Add your PayPal processing logic here
        elif payment_method == 'mpesa':
            mpesa_number = request.form.get('mpesa_number')
            # Add your M-Pesa processing logic here

        # Mark as paid and save payment method
        appointment.paid = True
        appointment.payment_method = payment_method
        db.session.commit()
        flash('Payment successful!', 'success')
        return redirect(url_for('auth.my_appointments'))
    return render_template('payment.html', appointment=appointment)
