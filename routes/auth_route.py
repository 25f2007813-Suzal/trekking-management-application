from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, logout_user, login_required
from controllers.auth_controller import login_user_logic, register_user
from models import Role

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        if current_user.role == Role.ADMIN:
            return redirect(url_for("admin.dashboard"))
        elif current_user.role == Role.STAFF:
            return redirect(url_for("staff.dashboard"))
        else:
            return redirect(url_for("user.dashboard"))
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


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        if current_user.role == Role.ADMIN:
            return redirect(url_for("admin.dashboard"))
        elif current_user.role == Role.STAFF:
            return redirect(url_for("staff.dashboard"))
        else:
            return redirect(url_for("user.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        role = request.form.get("role")
        name = request.form.get("name", "").strip()
        contact_details = request.form.get("contact_details", "").strip()

        if register_user(username, password, role, name, contact_details):
            flash("Registration successful! Please login.")
            return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
