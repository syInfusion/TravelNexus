from flask import Blueprint, render_template, redirect
from Nexus.auth import register, login

routes = Blueprint('routes', __name__)

@routes.route("/")
def home():
    return render_template('landing.html')

@routes.route("/login", methods=["GET"])
def login_page():
    return render_template('login.html')


@routes.route("/signup", methods=["GET", "POST"])
def signup_page():
    return render_template('signup.html')    