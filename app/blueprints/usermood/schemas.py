from marshmallow import fields, post_load, ValidationError
from app.models import db, UserMood, Feeling
from app.blueprints.feeling.schemas import FeelingSchema
from app.blueprints.mood.schemas import MoodSchema
from app.extensions import ma

class UserMoodSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = UserMood
    load_instance = True
    include_relationships = True
    sqla_session = db.session
    
  feelings = fields.List(fields.Integer(), required=True, load_only=True, attribute="feelings")
  
  feelings_info = fields.Nested(FeelingSchema, many=True, dump_only=True, attribute="feelings")
  
  mood_info = fields.Nested(MoodSchema, dump_only=True, attribute="mood")
  
  @post_load
  def load_feelings(self, data, **kwargs):
    if "feelings" in data:
      ids = data["feelings"]
      found = db.session.query(Feeling).filter(Feeling.id.in_(ids)).all()
      if len(found) != len(ids):
        raise ValidationError("One or more feeling IDs are invalid")
      data["feelings"] = found
    return data

usermood_schema = UserMoodSchema()
usermoods_schema = UserMoodSchema(many=True)
return_usermood_schema = UserMoodSchema(exclude=("mood",))