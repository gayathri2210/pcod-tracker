# project/auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash # Ensure both are here
from flask_login import login_user, logout_user, login_required, current_user # Ensure all are here
from .models import User
from .forms import LoginForm, RegistrationForm, ChangePasswordForm # Ensure all forms are imported
from . import db

auth = Blueprint('auth', __name__)

# --- Your existing @auth.route('/signup', ...) function ---
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(email=form.email.data.lower(),
                        username=form.username.data,
                        password_hash=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Your account has been created! You can now log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred while creating your account: {e}', 'danger') # Show specific error in flash for debug
            print(f"Error creating user: {e}") # Log specific error
    elif request.method == 'POST':
        flash('Please correct the errors below and try again.', 'warning')
    return render_template('signup.html', title='Sign Up', form=form)


# --- MODIFIED @auth.route('/login', ...) function with DEBUG PRINTS ---
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print("[LOGIN ROUTE] User already authenticated, redirecting to main.index.")
        return redirect(url_for('main.index'))

    form = LoginForm()
    print(f"[LOGIN ROUTE] Request method: {request.method}") # Log request method

    if request.method == 'POST':
        print(f"[LOGIN ROUTE] POST request received. Form data: {form.data}") # Log form data
        if form.validate_on_submit():
            print("[LOGIN ROUTE] Form validated successfully.")
            user_identifier = form.email_or_username.data
            password_entered = form.password.data
            print(f"[LOGIN ROUTE] Attempting to find user with identifier: '{user_identifier}'")
            
            # Try finding by email first (case-insensitive for email part)
            user_by_email = User.query.filter(User.email == user_identifier.lower()).first()
            
            user_to_check = None
            if user_by_email:
                print(f"[LOGIN ROUTE] User found by email: {user_by_email.username} (ID: {user_by_email.id})")
                user_to_check = user_by_email
            else:
                print(f"[LOGIN ROUTE] User not found by email, trying username: '{user_identifier}'")
                user_by_username = User.query.filter(User.username == user_identifier).first()
                if user_by_username:
                    print(f"[LOGIN ROUTE] User found by username: {user_by_username.username} (ID: {user_by_username.id})")
                    user_to_check = user_by_username
            
            if user_to_check:
                print(f"[LOGIN ROUTE] Checking password for user '{user_to_check.username}'.")
                if check_password_hash(user_to_check.password_hash, password_entered):
                    print(f"[LOGIN ROUTE] Password MATCH for user '{user_to_check.username}'. Logging in.")
                    login_user(user_to_check, remember=form.remember.data)
                    next_page = request.args.get('next')
                    flash('Login successful!', 'success')
                    print(f"[LOGIN ROUTE] Redirecting to next_page: '{next_page}' or main.index.")
                    return redirect(next_page) if next_page else redirect(url_for('main.index'))
                else:
                    print(f"[LOGIN ROUTE] Password MISMATCH for user '{user_to_check.username}'.")
                    flash('Login unsuccessful. Incorrect password provided.', 'danger')
            else:
                print(f"[LOGIN ROUTE] User NOT FOUND with identifier: '{user_identifier}'")
                flash('Login unsuccessful. User with that email/username not found.', 'danger')
        else: # form.validate_on_submit() was False for a POST request
            print(f"[LOGIN ROUTE] Form validation FAILED. Errors: {form.errors}")
            flash('Login unsuccessful. Please correct the errors shown below.', 'warning')
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"[LOGIN ROUTE] Validation Error in field '{field}': {error}")
            
    # This is reached for GET requests or if a POST request didn't result in a redirect
    return render_template('login.html', title='Login', form=form)


# --- Your existing @auth.route('/change_password', ...) function ---
@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if check_password_hash(current_user.password_hash, form.current_password.data):
            current_user.password_hash = generate_password_hash(form.new_password.data, method='pbkdf2:sha256')
            db.session.commit()
            flash('Your password has been successfully updated!', 'success')
            return redirect(url_for('main.profile'))
        else:
            flash('Incorrect current password. Please try again.', 'danger')
    elif request.method == 'POST':
         flash('Please correct the errors shown below.', 'warning')
    return render_template('change_password.html', title='Change Password', form=form)


# --- Your existing @auth.route('/logout', ...) function ---
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out.', 'info')
    return redirect(url_for('main.index'))
