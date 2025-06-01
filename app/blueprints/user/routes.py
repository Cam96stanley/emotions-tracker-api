from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from app.models import db, User
from app.blueprints.user import user_bp
from app.utils.auth import hash_password
from app.blueprints.user.schemas import create_user_schema, return_user_schema, user_schema

@user_bp.route("/", methods=["POST"])
def create_user():
  try:
    user_data = create_user_schema.load(request.json)
    
    hashed_pw = hash_password(user_data["password"])
    
    new_user = User(
      name=user_data["name"],
      email=user_data["email"],
      password=hashed_pw,
      is_admin=user_data.get("is_admin", False),
      image=user_data.get("image", "uploads/default_user.png")
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(return_user_schema.dump(new_user)), 201
    
  except ValidationError as e:
    return jsonify(e.messages), 400
  
  except IntegrityError as e:
    db.session.rollback()
    
    if "unique constraint" in str(e).lower() or "duplicate key" in str(e).lower():
      return jsonify({"error": "Email already registered"}), 409
    
    return jsonify({"error": "Database error"}), 500