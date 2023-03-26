from flask import Blueprint, request, jsonify
from flask_login import login_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Organization
from sqlalchemy.exc import IntegrityError
from . import db
from . import permify


auth = Blueprint("auth", __name__)


@auth.post("/login")
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    user = User.query.filter_by(email=email).first()
    if user :
        if check_password_hash(user.password, password):
            login_user(user, remember=True)
            return (
                 jsonify(
                     {
                         "status" : "SUCCESS",
                         "message": "User logged in successfully",
                     }
                 ),
                 200,
            )
        else:
            return (
                jsonify(
                    {
                        "status" : "error",
                        "message" : "Incorrect password",
                    }
                ),
                400,
            )
    else:
        return(
            jsonify(
                {
                    "status": "error",
                    "message": "User does not exist",
                }
            ),
            400,
        )    

@auth.get("/me")
def me():
    if current_user.is_authenticated:
        return(
            jsonify(
                {
                    "status": "SUCCESS",
                    "message" : "User logged in successfully",
                    "data" : {"username" : current_user.username },
                }
            ),
            200,
        )
    else:
        return(
            jsonify(
                {
                    "status": "ERROR",
                    "message": "Not authenticated",
                }
            ),
            400,
        )

@auth.post("/register")
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password_1 = data.get("password-1")
    password_2 = data.get("password-2")
    if password_1 != password_2:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Password does not match",
                }
            ),
            400,
        )
    else:
        user = User(
            email = email,
            username=username,
            password=generate_password_hash(password_1, "sha256")
        )
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            print(f"An Error occurred {e}")
        else:
            login_user(user, remember=True)
            return(
                jsonify(
                    {
                        "status": "SUCCESS",
                        "message": "User logged in successfully",
                    }
                ),
                200,
            )