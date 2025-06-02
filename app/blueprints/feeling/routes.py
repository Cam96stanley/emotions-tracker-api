from flask import request, jsonify
from marshmallow import ValidationError
from app.models import db, Feeling, UserMood
from app.blueprints.feeling import feeling_bp
from app.blueprints.feeling.schemas import feeling_schema, feelings_schema

@feeling_bp.route("/", methods=["POST"])
def create_feeling():
  try:
    feeling_data = feeling_schema.load(request.json)
    
    db.session.add(feeling_data)
    db.session.commit()
    
    return jsonify(feeling_schema.dump(feeling_data)), 201
  
  except ValidationError as e:
    return jsonify(e.messages), 400