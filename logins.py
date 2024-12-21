from flask import Flask, redirect, url_for, flash, session
from flask_login import current_user
from db import User


def admin_required(f):
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:  # Check if the user is logged in
            flash("Please log in to access this page.", "danger")
            return redirect(url_for("login"))

        if not current_user.is_admin:  # If the user is not an admin, deny access
            flash("You do not have permission to access this page.", "danger")
            return redirect(url_for("home"))

        return f(*args, **kwargs)
    wrap.__name__ = f.__name__  # To avoid issues with wrapped functions
    return wrap
