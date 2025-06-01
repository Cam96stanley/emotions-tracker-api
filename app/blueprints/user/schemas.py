from app.extensions import ma
from app.models import User

class UserSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = User
    load_instance = True

create_user_schema = UserSchema()
return_user_schema = UserSchema(exclude=("password",))
return_users_schema = UserSchema(many=True, exclude=("password",))
update_user_schema = UserSchema(partial=True)
users_schema = UserSchema(many=True)