from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    create_refresh_token,
    get_jwt,
    unset_jwt_cookies,
)
import datetime
from app import bcrypt
from .models import Alias, db

ACCESS_EXPIRES = datetime.timedelta(days=1)

auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["POST"])
def signup():
    body = request.get_json()
    alias = body.get("alias")
    email = body.get("email")
    password = body.get("password")

    password = str(password)
    if not email or not alias or not password:
        return jsonify({"Message": "Missing required fields"}), 400

    if len(alias) < 4:
        return jsonify({"msg": "alias too short"}), 400

    if len(password) < 5:
        return jsonify({"message": "Password too short"})

    if len(email) < 5:
        return jsonify({"message": "email too short"})
    hashed_password = bcrypt.generate_password_hash(password).decode("utf8")

    new_alias = Alias(alias=alias, email=email, password=hashed_password)

    db.session.add(new_alias)
    db.session.commit()

    return jsonify({"Message": "Success"}), 201


@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    password = str(password)

    if not email or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    if not email or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    alias = Alias.query.filter_by(email=email).first()

    if alias and bcrypt.check_password_hash(alias.password, password):
        access_token = create_access_token(
            identity=alias.id, expires_delta=ACCESS_EXPIRES
        )
        refresh_token = create_refresh_token(identity=alias.id)

        print("acess", access_token)
        print(access_token)
        return (
            jsonify(
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
            ),
            200,
        )

    return jsonify({"msg": "Invalid email or password"}), 401


@auth.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    unset_jwt_cookies()
    return jsonify({"msg": "Logged out successfully"}), 200
