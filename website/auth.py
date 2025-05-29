from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, db
from flask_login import login_user, logout_user, current_user, login_required
from .service import SignUpInput, UserService, LoginInput


auth = Blueprint('auth', __name__)


@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email=request.form.get('email')
        username=request.form.get('username')
        password=request.form.get('passw1')
        passw2=request.form.get('passw2')

        valid, message = SignUpInput.is_input_valid(password, passw2, username, email)
        if not valid:
            flash(message, 'error')
            render_template('signup.html', user=current_user)

        message, user = SignUpInput.sign_up(email, username, password)  # type: ignore[call-args]

        if not user:
            flash(message, 'error')
        else:
            flash(message, 'success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))


    return render_template('signup.html', user=current_user)

@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')

        valid, message = LoginInput.is_valid(email, password)
        if not valid:
            flash(message, 'error')
            return render_template('login.html', user=current_user)

        user = UserService.get_user_by_email(email)  # type: ignore[call-args]

        if not user:
            flash(f'No user found with matching email: {email}', 'error')
            return render_template('login.html', user=current_user)

        if not check_password_hash(user.password, password):  # type: ignore[call-args]
            flash('The given password does not match the existing one, please try again', 'error')
            return render_template('login.html', user=current_user)

        login_user(user, remember=True)
        flash('Login successful', 'success')
        return redirect(url_for('views.home'))

    return render_template('login.html', user=current_user)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/modify-user/<int:user_id>', methods=["POST"])
@login_required
def modify_user(user_id):
    user = User.query.get(int(user_id))
    if not user:
        raise ValueError(f"No user found with user id: {user_id}")

    username = request.form.get('username')
    email = request.form.get('email')

    if email:
        user.email = email
    if username:
        user.username = username
    db.session.commit()

    return render_template('profilepage.html', user=current_user)