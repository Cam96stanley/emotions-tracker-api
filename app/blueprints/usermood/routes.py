from flask import request, jsonify
from marshmallow import ValidationError
from app.blueprints.usermood import usermood_bp
from app.models import db, UserMood
from app.blueprints.usermood.schemas import usermood_schema, usermoods_schema
from app.utils.auth import token_required

@usermood_bp.route("/", methods=["POST"])
@token_required
def create_usermood(user_id):
  data = request.json
  
  data["user"] = user_id
  
  required_fields = ["sleep_time", "user", "mood", "feelings"]
  missing = [field for field in required_fields if field not in data]
  
  if missing:
    return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400
  
  if not isinstance(data["feelings"], list) or not data["feelings"]:
    return jsonify({"error": "'feelings' must be a non-empty list of IDs"}), 400
  
  try:
    usermood_data = usermood_schema.load(data)
    
    db.session.add(usermood_data)
    db.session.commit()
    
    return jsonify(usermood_schema.dump(usermood_data)), 201
  
  except ValidationError as e:
    return jsonify(e.messages), 400


@usermood_bp.route("/", methods=["GET"])
@token_required
def get_users_usermoods(user_id):
  usermoods = UserMood.query.filter_by(user_id=user_id).all()
  
  if not usermoods:
    return jsonify({"message": "No moods found for this user."}), 404
  
  return jsonify(usermoods_schema.dump(usermoods)), 200


@usermood_bp.route("/<int:usermood_id>", methods=["DELETE"])
@token_required
def delete_usermood(user_id, usermood_id):
  usermood = UserMood.query.get(usermood_id)
  
  if not usermood:
    return jsonify({"message": "UserMood not found"}), 404
  
  if usermood.user_id != int(user_id):
    return jsonify({"message": "User is not authorized to delete this UserMood"}), 403
  
  db.session.delete(usermood)
  db.session.commit()
  return jsonify({"message": "UserMood deleted successfully"}), 200