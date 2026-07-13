from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile", methods=["GET", "POST"])
@login_required
def update_profile():
    if request.method == "POST":
        current_user.name = request.form.get("name", "").strip()
        current_user.contact_details = request.form.get("contact_details", "").strip()

        new_password = request.form.get("password", "").strip()
        if new_password:

            if len(new_password) < 8 or len(new_password) > 15:
                flash("Password must be between 8 and 15 characters.")
                return render_template("profile.html")
            current_user.password = new_password

        db.session.commit()
        flash("Profile updated successfully!")
        return redirect(url_for("profile.update_profile"))

    return render_template("profile.html")
