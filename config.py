from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from the .env file

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'defaultsecretkey')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///users.db')  # Default SQLite URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable Flask-SQLAlchemy modification tracking

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"  # Redirect to login page if not authenticated
