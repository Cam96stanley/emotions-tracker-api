from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from app.models import db, User
from app.blueprints.user import user_bp
from app.utils.auth import hash_password
from app.blueprints.user.schemas import create_user_schema, return_user_schema

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