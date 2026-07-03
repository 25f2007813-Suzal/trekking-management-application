from flask import Flask
from models import db, User, Role


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trek_app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

        admin = User.query.filter_by(role=Role.ADMIN).first()
        if not admin:
            admin = User(
                username="admin",
                password="admin123",
                role=Role.ADMIN,
                is_approved=True,
            )
            db.session.add(admin)
            db.session.commit()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
