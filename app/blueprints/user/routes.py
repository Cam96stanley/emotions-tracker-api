from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from app.models import db, User
from app.blueprints.user import user_bp
from app.utils.auth import hash_password
from app.blueprints.user.schemas import create_user_schema, return_user_schema, return_users_schema, update_user_schema

@user_bp.route("/", methods=["POST"])
def create_user():
  try:
    user_data = create_user_schema.load(request.json)
    
    user_data.password = hash_password(user_data.password)
    
    db.session.add(user_data)
    db.session.commit()
    
    return jsonify(return_user_schema.dump(user_data)), 201
    
  except ValidationError as e:
    return jsonify(e.messages), 400
  
  except IntegrityError as e:
    db.session.rollback()
    
    if "unique constraint" in str(e).lower() or "duplicate key" in str(e).lower():
      return jsonify({"error": "Email already registered"}), 409
    
    return jsonify({"error": "Database error"}), 500


@user_bp.route("/", methods=["GET"])
def get_users():
  query = db.session.query(User)
  users = db.session.execute(query).scalars().all()
  
  if users is None:
    return jsonify({"messages": "No users found"}), 404
  
  return jsonify(return_users_schema.dump(users)), 200


@user_bp.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
  query = db.session.query(User).where(User.id == user_id)
  user = db.session.execute(query).scalars().first()
  
  if user is None:
    return jsonify({"message": "No user found with that id"}), 404
  
  return jsonify(return_user_schema.dump(user)), 200


@user_bp.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
  user = db.session.get(User, user_id)
  if not user:
    return jsonify({"error": "User not found"}), 404
  
  data = request.json
  
  if "name" in data:
    user.name = data["name"]
  if "email" in data:
    user.email = data["email"]
  if "password" in data:
    user.password = hash_password(data["password"])
  if "image" in data:
    user.image = data["image"]
  if "is_admin" in data:
    user.is_admin = data["is_admin"]
  
  try:
    db.session.commit()
    return jsonify(return_user_schema.dump(user)), 200
  except IntegrityError:
    db.session.rollback()
    return jsonify({"error": "Email already in use"}), 409
  except Exception:
    db.session.rollback()
    return jsonify({"error": "Database error"}), 500


@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
  user = db.session.get(User, user_id)
  
  if not user:
    return jsonify({"message": "User not found"}), 404
  
  db.session.delete(user)
  db.session.commit()
  
  return jsonify({"message": f"User {user.id} deleted successfully"}), 200