from app.models import Feeling
from app.extensions import ma

class FeelingSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = Feeling
    load_instance = True
    include_fk = True

feeling_schema = FeelingSchema()
feelings_schema = FeelingSchema(many=True)