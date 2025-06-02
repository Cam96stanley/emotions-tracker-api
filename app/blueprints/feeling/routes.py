from flask import request, jsonify
from marshmallow import ValidationError
from app.models import db, Feeling
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


@feeling_bp.route("/", methods=["GET"])
def get_feelings():
  query = db.session.query(Feeling)
  feelings = db.session.execute(query).scalars().all()
  
  if not feelings:
    return jsonify({"message": "No feelings found"}), 404
  
  return jsonify(feelings_schema.dump(feelings)), 200


@feeling_bp.route("/<int:feeling_id>", methods=["DELETE"])
def delete_feeling(feeling_id):
  feeling = db.session.get(Feeling, feeling_id)
  
  if not feeling:
    return jsonify({"message": "No feeling with that id"}), 404
  
  db.session.delete(feeling)
  db.session.commit()  
  
  return jsonify({"message": f"Feeling {feeling_id} deleted successfully"}), 200