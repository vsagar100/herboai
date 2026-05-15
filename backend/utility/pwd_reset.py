import argparse
import os
import sys

from flask import Flask
from werkzeug.security import generate_password_hash

_HERE = os.path.dirname(os.path.abspath(__file__))
_BACKEND_ROOT = os.path.dirname(_HERE)
if _BACKEND_ROOT not in sys.path:
    sys.path.insert(0, _BACKEND_ROOT)

from config import Config
from db import init_app as init_db, get_db


def _build_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    init_db(app)
    return app


def reset_admin_password(new_password: str) -> int:
    app = _build_app()
    with app.app_context():
        db = get_db()
        pw_hash = generate_password_hash(new_password)
        cur = db.execute(
            "UPDATE admin_users SET password_hash = ? WHERE username = ?",
            (pw_hash, "admin"),
        )
        db.commit()
        return cur.rowcount


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reset the admin user's password in admin_users."
    )
    parser.add_argument(
        "--password",
        required=True,
        help="New password for username=admin",
    )
    args = parser.parse_args()

    updated = reset_admin_password(args.password)
    if updated == 0:
        print("No admin user found with username=admin.")
        return 1

    print("Admin password updated successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
