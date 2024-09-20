from flask import Blueprint, render_template, redirect, url_for, flash, request
from Nexus.auth import register, login
from Nexus.forms import SignupForm, LoginForm

routes = Blueprint('routes', __name__)

@routes.route("/")
def home():
    return render_template('landing.html')

@routes.route("/login", methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        data = {
            'email': form.email.data,
            'password': form.password.data
        }
        response = login()
        if response.status_code == 200:
            flash('Logged in successfully', 'success')
            return redirect(url_for('routes.home'))
        else:
            flash(response.json['message'], 'danger')
    return render_template('login.html', form=form)

@routes.route("/signup", methods=["GET", "POST"])
def signup_page():
    form = SignupForm()
    if form.validate_on_submit():
        data = {
            'username': form.username.data,
            'email': form.email.data,
            'password': form.password.data
        }
        response = register()
        if response.status_code == 201:
            flash('Account created successfully', 'success')
            return redirect(url_for('routes.login_page'))
        else:
            flash(response.json['message'], 'danger')
    return render_template('signup.html', form=form)
