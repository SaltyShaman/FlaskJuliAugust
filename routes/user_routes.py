#Svarer til en controller i Java
#routes/user_routes.py

from flask import Blueprint, jsonify, request
from services.user_service import get_all_users, add_user, get_user_by_id, update_user, delete_user
from test_data.dummy_users import dummy_users

user_bp = Blueprint('user_bp', __name__)

from flask import Blueprint, jsonify, request
from services.user_service import get_all_users, add_user, get_user_by_id, update_user, delete_user

user_bp = Blueprint('user_bp', __name__)

@user_bp.route("/", methods=["GET"])
def get_users():
    users = get_all_users()
    return jsonify([user.__dict__ if hasattr(user, '__dict__') else user for user in users])

@user_bp.route("/", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = add_user(data)
    if "error" in new_user:
        return jsonify(new_user), 400
    return jsonify(new_user.__dict__ if hasattr(new_user, '__dict__') else new_user), 201

@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user_by_id_route(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify(user.__dict__ if hasattr(user, '__dict__') else user)
    else:
        return jsonify({"error": "User not found"}), 404

@user_bp.route("/<int:user_id>", methods=["PUT"])
def update_user_route(user_id):
    data = request.get_json()
    updated_user = update_user(user_id, data)
    if "error" in updated_user:
        return jsonify(updated_user), 400
    return jsonify(updated_user.__dict__ if hasattr(updated_user, '__dict__') else updated_user)

@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user_route(user_id):
    result = delete_user(user_id)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)