from flask import Blueprint, flash, render_template, request, redirect, url_for, abort
from flask_login import current_user, login_required

from controllers.staff_controller import get_assigned_trek, update_trek_status_and_slots
from models import db, Booking, BookingStatus, Role, Trek

staff_bp = Blueprint("staff", __name__)


@staff_bp.route("/staff/dashboard")
@login_required
def dashboard():
    if current_user.role != Role.STAFF:
        abort(403)

    query = request.args.get("q", "").strip()
    treks = get_assigned_trek(current_user.id, query)
    return render_template("staff_dash.html", treks=treks)


@staff_bp.route("/staff/update-trek/<int:trek_id>", methods=["POST"])
@login_required
def update_trek(trek_id):
    if current_user.role != Role.STAFF:
        abort(403)

    new_status = request.form.get("status")
    new_slots = request.form.get("slots")
    update_trek_status_and_slots(trek_id, current_user.id, new_status, new_slots)
    flash("Trek updated!")
    return redirect(url_for("staff.dashboard"))


@staff_bp.route("/staff/trek/<int:trek_id>/participats")
@login_required
def trek_participants(trek_id):
    if current_user.role != Role.STAFF:
        abort(403)

    trek = Trek.query.filter(
        Trek.id == trek_id, Trek.staff_id == current_user.id
    ).first_or_404()

    return render_template("staff_participants.html", trek=trek)


@staff_bp.route("/staff/cancel-participant/<int:booking_id>", methods=["POST"])
@login_required
def cancel_participant(booking_id):
    if current_user.role != Role.STAFF:
        abort(403)

    booking = Booking.query.filter_by(id=booking_id).first()
    if booking and booking.trek.staff_id == current_user.id:
        booking.status = BookingStatus.CANCELLED
        booking.trek.available_slots += 1
        db.session.commit()
        flash("Participant booking cancelled.")
    return redirect(url_for("staff.trek_participants", trek_id=booking.trek_id))
