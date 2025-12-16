from flask import Blueprint, request, jsonify, current_app
from models import User
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from sqlalchemy.exc import IntegrityError, OperationalError
from extensions import db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

# --------------------------------------------------
# REGISTER
# --------------------------------------------------
@auth_bp.route("/register", methods=["POST", "OPTIONS"])
def register():
    if request.method == "OPTIONS":
        return "", 200

    data = request.get_json(silent=True) or {}

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify(error="Username, email and password are required"), 400

    try:
        user = User(username=username, email=email)
        user.password = password

        db.session.add(user)
        db.session.commit()

        return jsonify(message="User registered successfully"), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify(error="Username or email already exists"), 409

    except OperationalError as e:
        # 🔥 THIS IS THE MISSING FIX
        current_app.logger.warning(
            f"DB connection lost during register — disposing engine: {e}"
        )

        db.session.rollback()
        db.engine.dispose()   # ← kills broken SSL connections

        return jsonify(
            error="Temporary database issue — please retry"
        ), 503

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Unexpected error in register: {e}")
        return jsonify(error="Server error"), 500

# --------------------------------------------------
# LOGIN
# --------------------------------------------------
@auth_bp.route("/login", methods=["POST", "OPTIONS"])
def login():
    if request.method == "OPTIONS":
        return "", 200

    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify(error="Email and password required"), 400

    try:
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            token = create_access_token(identity=user.id)
            return jsonify(access_token=token, username=user.username), 200

        return jsonify(error="Invalid email or password"), 401

    except OperationalError as e:
        db.session.rollback()
        db.engine.dispose()
        current_app.logger.warning(f"DB lost during login: {e}")
        return jsonify(error="Temporary database issue"), 503
