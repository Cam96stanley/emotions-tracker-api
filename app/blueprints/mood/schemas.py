from app.models import Mood
from app.extensions import ma

class MoodSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Mood

mood_schema = MoodSchema()