from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import logout_user, login_required
from controllers.auth_controller import login_user_logic, register_user
from models import Role

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        user = login_user_logic(username, password)

        if user:
            if user.role == Role.ADMIN:
                return redirect(url_for("admin.dashboard"))
            if user.role == Role.STAFF:
                return redirect(url_for("staff.dashboard"))
            return redirect(url_for("user.dashboard"))

        flash("Invalid credentials")

    return render_template("login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        role = request.form.get("role")

        if register_user(username, password, role):
            flash("Registration successful! Please login.")
            return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
