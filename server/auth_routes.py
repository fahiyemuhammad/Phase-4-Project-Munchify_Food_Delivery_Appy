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
        new_user = User(username=username, email=email)
        new_user.password = password  # triggers hashing + validation

        db.session.add(new_user)
        db.session.commit()

        return jsonify(message="User registered successfully"), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify(error="Username or email already exists"), 409

    except OperationalError as e:
        db.session.rollback()
        current_app.logger.warning(
            f"DB connection lost during register (will recover): {str(e)}"
        )
        return jsonify(
            error="Temporary database issue — please try again"
        ), 503

    except ValueError as e:
        db.session.rollback()
        return jsonify(error=str(e)), 400

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(
            f"Unexpected error in register: {str(e)}"
        )
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
        return jsonify(error="Email and password are required"), 400

    try:
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return (
                jsonify(
                    access_token=access_token,
                    username=user.username,
                ),
                200,
            )

        return jsonify(error="Invalid email or password"), 401

    except OperationalError as e:
        db.session.rollback()
        current_app.logger.warning(
            f"DB connection lost during login: {str(e)}"
        )
        return jsonify(
            error="Temporary database issue — please try again"
        ), 503


# --------------------------------------------------
# GET CURRENT USER
# --------------------------------------------------
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()

    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify(error="User not found"), 404

        return (
            jsonify(
                id=user.id,
                username=user.username,
                email=user.email,
            ),
            200,
        )

    except OperationalError as e:
        db.session.rollback()
        current_app.logger.warning(
            f"DB connection lost during /me: {str(e)}"
        )
        return jsonify(
            error="Temporary database issue — please try again"
        ), 503


# --------------------------------------------------
# UPDATE CURRENT USER
# --------------------------------------------------
@auth_bp.route("/update", methods=["PATCH", "OPTIONS"])
@jwt_required()
def update_user():
    if request.method == "OPTIONS":
        return "", 200

    user_id = get_jwt_identity()
    data = request.get_json(silent=True) or {}

    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify(error="User not found"), 404

        if "email" in data:
            return jsonify(error="Email cannot be changed"), 400

        if "username" in data and data["username"].strip():
            user.username = data["username"]

        if "password" in data and data["password"].strip():
            user.password = data["password"]

        db.session.commit()
        return jsonify(message="User updated successfully"), 200

    except IntegrityError:
        db.session.rollback()
        return jsonify(error="Username already taken"), 409

    except OperationalError as e:
        db.session.rollback()
        current_app.logger.warning(
            f"DB connection lost during update: {str(e)}"
        )
        return jsonify(
            error="Temporary database issue — please try again"
        ), 503

    except ValueError as e:
        db.session.rollback()
        return jsonify(error=str(e)), 400

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(
            f"Unexpected error in update: {str(e)}"
        )
        return jsonify(error="Server error"), 500


# --------------------------------------------------
# DELETE CURRENT USER
# --------------------------------------------------
@auth_bp.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()

    try:
        user = User.query.get(user_id)

        if not user:
            return jsonify(error="User not found"), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify(message="User deleted successfully"), 200

    except OperationalError as e:
        db.session.rollback()
        current_app.logger.warning(
            f"DB connection lost during delete: {str(e)}"
        )
        return jsonify(
            error="Temporary database issue — please try again"
        ), 503

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(
            f"Unexpected error in delete: {str(e)}"
        )
        return jsonify(error="Server error"), 500
