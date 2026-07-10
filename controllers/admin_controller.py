from datetime import datetime, timedelta

from models import db, Booking, Role, Trek, User, Difficulty, TrekStatus


def get_admin_stats():
    return {
        "treks": Trek.query.count(),
        "users": User.query.filter(User.role == Role.TREKKER).count(),
        "staff": User.query.filter(User.role == Role.STAFF).count(),
        "bookings": Booking.query.count(),
    }


def search_system_users(query):
    if query.isdigit():
        users = User.query.filter(User.id == int(query)).all()
    else:
        users = User.query.filter(User.username.ilike(f"%{query}%")).all()

    return users


def search_system_treks(query):
    if query.isdigit():
        treks = Trek.query.filter(Trek.id == int(query)).all()
    else:
        treks = Trek.query.filter(Trek.name.ilike(f"%{query}%")).all()

    return treks


def toggle_user_status(user_id):
    user = User.query.get(user_id)

    if user:
        user.is_active = not user.is_active
        db.session.commit()

    return user


def approve_staff(staff_id):
    staff = User.query.get(staff_id)

    if staff:
        staff.is_approved = True
        db.session.commit()

    return staff


def create_new_trek(data):
    start_date = datetime.strptime(data["start_date"], "%Y-%m-%d")

    end_date = start_date + timedelta(days=int(data["duration"]))

    new_trek = Trek(
        name=data["name"],
        location=data["location"],
        difficulty=Difficulty[data["difficulty"]],
        duration=int(data["duration"]),
        available_slots=int(data["slots"]),
        status=TrekStatus.PENDING,
        start_date=start_date,
        end_date=end_date,
    )

    db.session.add(new_trek)
    db.session.commit()


def update_trek(trek_id, data):
    trek = Trek.query.get(trek_id)
    if trek:
        trek.name = data["name"]
        trek.location = data["location"]
        trek.difficulty = Difficulty[data["difficulty"]]
        trek.available_slots = max(0, int(data["slots"]))
        staff_id = data.get("staff_id")
        trek.staff_id = int(staff_id) if staff_id else None

        db.session.commit()
    return trek


def get_pending_staff():
    return User.query.filter_by(role=Role.STAFF, is_approved=False).all()


def get_all_bookings():
    return Booking.query.all()
