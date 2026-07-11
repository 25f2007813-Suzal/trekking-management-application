from flask import Blueprint, abort, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required

from controllers.user_controllers import (
    get_available_treks,
    book_user_trek,
    get_user_bookings,
    cancel_user_trek,
    get_user_history,
)
from models import Role

user_bp = Blueprint("user", __name__)


@user_bp.route("/user/dashboard")
@login_required
def dashboard():
    if current_user.role != Role.TREKKER:
        abort(403)

    query = request.args.get("q", "").strip()
    difficulty = request.args.get("difficulty")

    treks = get_available_treks(query, difficulty)

    return render_template("user_dash.html", treks=treks)


@user_bp.route("/user/book/<int:trek_id>", methods=["POST"])
@login_required
def book_trek(trek_id):
    if current_user.role != Role.TREKKER:
        abort(403)

    message = book_user_trek(current_user.id, trek_id)
    flash(message)
    return redirect(url_for("user.dashboard"))


@user_bp.route("/user/my-bookings")
@login_required
def my_bookings():
    if current_user.role != Role.TREKKER:
        abort(403)

    bookings = get_user_bookings(current_user.id)
    return render_template("user_bookings.html", bookings=bookings)


@user_bp.route("/user/cancel/<int:booking_id>", methods=["POST"])
@login_required
def cancel_booking(booking_id):
    if current_user.role != Role.TREKKER:
        abort(403)

    message = cancel_user_trek(booking_id, current_user.id)
    flash(message)
    return redirect(url_for("user.my_bookings"))


@user_bp.route("/user/history")
@login_required
def history():
    bookings = get_user_history(current_user.id)
    return render_template("user_history.html", bookings=bookings)
