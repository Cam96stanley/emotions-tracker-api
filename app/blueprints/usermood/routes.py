from flask import request, jsonify
from marshmallow import ValidationError
from app.blueprints.usermood import usermood_bp
from app.models import db, UserMood
from app.blueprints.usermood.schemas import usermood_schema, usermoods_schema

@usermood_bp.route("/", methods=["POST"])
def create_usermood():
  data = request.json
  print("Recieved data:", data)
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