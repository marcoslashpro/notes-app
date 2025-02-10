from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, db
from flask_login import login_user, logout_user, current_user, login_required
from .service import SignUpInput, UserService, LoginInput


auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        signup_input = SignUpInput(
            email=request.form.get('email'),
            username=request.form.get('username'),
            passw1=request.form.get('passw1'),
            passw2=request.form.get('passw2')
            )

        if signup_input.is_valid():
                user = UserService.create_User(
                    email=signup_input.email,
                    password=signup_input.hash_password(),
                    username=signup_input.username
                    )
                if user:
                    flash('Sign up successfull', 'success')
                    redirect(url_for('views.home'))
                else:
                    flash('Something went wrong with the signup, please try again.', 'error')

    return render_template('signup.html', user=current_user)


@auth.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_input = LoginInput(
            email=request.form.get('email'),
            password=request.form.get('password')
        )

        print(f"Input Email: {login_input.email}, Input Password: {login_input.password}")

        if login_input.is_valid():
            user = UserService.user_exists(login_input.email)

            if user and check_password_hash(user.password, login_input.password):
                login_user(user, remember=True)
                flash('Login successful', 'success')
                return redirect(url_for('views.home'))
            else:
                flash('Invalid email or password', 'error')

    return render_template('login.html', user=current_user)



@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

from flask_login import login_user

@auth.route('/modify-user/<int:user_id>', methods=["POST"])
@login_required
def modify_user(user_id):
    user = User.query.get(int(user_id))

    username = request.form.get('username')
    email = request.form.get('email')

    if email:
        user.email = email
    if username:
        user.username = username
    db.session.commit()

    return render_template('profilepage.html', user=current_user)