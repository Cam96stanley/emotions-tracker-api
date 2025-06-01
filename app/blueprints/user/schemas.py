from app.extensions import ma
from app.models import User

class UserSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = User
    load_instance = True

create_user_schema = UserSchema()
return_user_schema = UserSchema(exclude=("password", "id"))
users_schema = UserSchema(many=True)