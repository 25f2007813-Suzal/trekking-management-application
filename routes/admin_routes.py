from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from flask_login import current_user, login_required

from controllers.admin_controller import (
    approve_staff,
    create_new_trek,
    get_admin_stats,
    get_all_bookings,
    get_pending_staff,
    search_system_treks,
    search_system_users,
    toggle_user_status,
    update_trek,
)
from models import Role, Trek, User, db

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/dashboard")
@login_required
def dashboard():
    if current_user.role != Role.ADMIN:
        abort(403)

    query = request.args.get("q")

    if query:
        users = search_system_users(query)
    else:
        users = User.query.all()

    stats = get_admin_stats()
    return render_template("admin_dash.html", stats=stats, users=users)


@admin_bp.route("/admin/approve-staff/<int:id>")
@login_required
def approve(id):
    if current_user.role != Role.ADMIN:
        abort(403)

    approve_staff(id)
    flash("Staff approved successfully.")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/admin/toggle_status/<int:id>")
@login_required
def toggle_status(id):
    if current_user.role != Role.ADMIN:
        abort(403)

    toggle_user_status(id)
    flash("User status updated")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/admin/treks")
@login_required
def manage_treks():
    if current_user.role != Role.ADMIN:
        abort(403)

    query = request.args.get("q")

    if query:
        treks = search_system_treks(query)
    else:
        treks = Trek.query.all()
    return render_template("admin_manage_trek.html", treks=treks)


@admin_bp.route("/admin/add-trek", methods=["POST"])
@login_required
def add_trek():

    if current_user.role != Role.ADMIN:
        abort(403)
    create_new_trek(request.form)
    flash("Trek created successfully!")
    return redirect(url_for("admin.manage_treks"))


@admin_bp.route("/admin/delete-trek/<int:id>")
@login_required
def delete_trek(id):
    if current_user.role != Role.ADMIN:
        abort(403)
    trek = Trek.query.get_or_404(id)

    db.session.delete(trek)
    db.session.commit()
    flash("Trek deleted successfully")

    return redirect(url_for("admin.manage_treks"))


@admin_bp.route("/admin/edit-trek/<int:id>", methods=["GET", "POST"])
@login_required
def edit_trek(id):
    if current_user.role != Role.ADMIN:
        abort(403)
    trek = Trek.query.get_or_404(id)
    staff_members = User.query.filter_by(role=Role.STAFF, is_approved=True).all()

    if request.method == "POST":
        update_trek(id, request.form)
        flash("Trek updated successfully!")
        return redirect(url_for("admin.manage_treks"))

    return render_template(
        "admin_edit_trek.html", trek=trek, staff_members=staff_members
    )


@admin_bp.route("/admin/staff-applications")
@login_required
def staff_applications():
    if current_user.role != Role.ADMIN:
        abort(403)

    pending_staff = get_pending_staff()
    return render_template("admin_staff_apps.html", staff_list=pending_staff)


@admin_bp.route("/admin/bookings")
@login_required
def view_all_bookings():
    if current_user.role != Role.ADMIN:
        abort(403)

    bookings = get_all_bookings()
    return render_template("admin_bookings.html", bookings=bookings)
