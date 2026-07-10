from models import Trek, TrekStatus, db


def get_assigned_trek(staff_id, query):
    return Trek.query.filter(
        Trek.staff_id == staff_id, Trek.name.ilike(f"%{query}%")
    ).all()


def update_trek_status_and_slots(trek_id, staff_id, new_status, new_slots):
    trek = Trek.query.filter_by(id=trek_id, staff_id=staff_id).first()
    if trek:
        trek.status = TrekStatus[new_status]
        trek.available_slots = max(0, int(new_slots))
        db.session.commit()
    return trek


def get_trek_participants(trek_id, staff_id):
    trek = Trek.query.filter_by(id=trek_id, staff_id=staff_id).first()
    if trek:
        return trek.bookings
    return None
