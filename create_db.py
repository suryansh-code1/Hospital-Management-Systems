from app import create_app, db
from app.models import Admin
from werkzeug.security import generate_password_hash


def main():
    app = create_app()
    with app.app_context():
        db.create_all()
        # Seed predefined superuser admin if not exists
        if not Admin.query.filter_by(username="admin").first():
            admin = Admin(username="admin", password_hash=generate_password_hash("admin123"))
            db.session.add(admin)
            db.session.commit()
            print("Seeded admin user -> username: admin, password: admin123")
        else:
            print("Admin user already exists.")
        print("Database initialized.")


if __name__ == "__main__":
    main()
