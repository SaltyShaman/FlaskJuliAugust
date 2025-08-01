#Svarer til en controller i Java
#routes/user_routes.py

from flask import Blueprint, jsonify, request
from services.user_service import get_all_users, add_user
from test_data.dummy_users import dummy_users

user_bp = Blueprint('user_bp', __name__)

@user_bp.route("/", methods=["GET"])
def get_users():
    return jsonify(get_all_users())

@user_bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = add_user(data)
    return jsonify(new_user), 201
