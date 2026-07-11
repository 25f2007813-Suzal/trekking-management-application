from models import Booking, Trek, TrekStatus, db, BookingStatus


def get_available_treks(query, difficulty):
    if difficulty:
        treks = Trek.query.filter(
            Trek.name.ilike(f"%{query}%"),
            Trek.difficulty == difficulty,
            Trek.status == TrekStatus.OPEN,
        ).all()
    else:
        treks = Trek.query.filter(
            Trek.name.ilike(f"%{query}%"),
            Trek.status == TrekStatus.OPEN,
        ).all()

    return treks


def book_user_trek(user_id, trek_id):
    trek = Trek.query.get_or_404(trek_id)

    if trek.status != TrekStatus.OPEN:
        return "This trek is not open for booking."

    if trek.available_slots <= 0:
        return "This trek is full!"

    existing = Booking.query.filter_by(
        user_id=user_id, trek_id=trek_id, status=BookingStatus.BOOKED
    ).first()
    if existing:
        return "You have already booked this trek."

    new_booking = Booking(user_id=user_id, trek_id=trek_id, status=BookingStatus.BOOKED)
    trek.available_slots -= 1

    db.session.add(new_booking)
    db.session.commit()
    return "Booking successful!"


def get_user_bookings(user_id):
    return reversed(Booking.query.filter(Booking.user_id == user_id).all())


def cancel_user_trek(booking_id, user_id):
    booking = Booking.query.filter_by(id=booking_id, user_id=user_id).first()
    if booking and booking.status == BookingStatus.BOOKED:
        booking.status = BookingStatus.CANCELLED
        booking.trek.available_slots += 1
        db.session.commit()
        return "Booking cancelled successfully!"
    return "Booking could not be cancelled."


def get_user_history(user_id):
    return reversed(
        Booking.query.filter(
            Booking.user_id == user_id,
            Booking.status.in_([BookingStatus.COMPLETED, BookingStatus.CANCELLED]),
        ).all()
    )
