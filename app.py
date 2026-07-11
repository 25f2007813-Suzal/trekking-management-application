from flask import Flask
from models import db, User, Role
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trek_app.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "very_secret_key"

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

        admin = User.query.filter_by(role=Role.ADMIN).first()
        if not admin:
            admin = User(
                username="admin",
                password="admin123",
                role=Role.ADMIN,
                name="Admin",
                contact_details="trekkingapp@gmail.com",
                is_approved=True,
            )
            db.session.add(admin)
            db.session.commit()

    # routes setup
    from routes.auth_route import auth_bp
    from routes.admin_routes import admin_bp
    from routes.staff_routes import staff_bp
    from routes.user_routes import user_bp
    from routes.profile_routes import profile_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(profile_bp)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
