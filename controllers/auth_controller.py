from flask import flash
from flask_login import login_user
from models import db, User, Role


def register_user(username, password, role_str, name, contact_details):
    existing_user = User.query.filter(User.username == username).first()

    if existing_user:
        flash("Username already exits. Please choose another")
        return None

    if len(password) < 8 or len(password) > 15:
        flash("Password must be between 8 and 15 characters.")
        return None

    role = Role.STAFF if role_str == "Staff" else Role.TREKKER

    new_user = User(
        username=username,
        password=password,
        role=role,
        name=name,
        contact_details=contact_details,
        is_approved=(role == Role.TREKKER),
    )

    db.session.add(new_user)
    db.session.commit()

    return True


def login_user_logic(username, password):
    user = User.query.filter(User.username == username).first()

    if user and user.password == password:
        if not user.is_active:
            flash("Account in blacklisted")
            return None

        if user.role == Role.STAFF and not user.is_approved:
            flash("Wait for Admin approval.")
            return None

        login_user(user)
        return user

    return None
