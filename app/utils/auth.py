from flask_bcrypt import Bcrypt
from jose import jwt
import datetime
from datetime import timedelta
from flask import current_app

bcrypt = Bcrypt()

def hash_password(plain_password: str) -> str:
  return bcrypt.generate_password_hash(plain_password).decode("utf-8")

def check_password(plain_password: str, hashed_password: str) -> bool:
  return bcrypt.check_password_hash(hashed_password, plain_password)

def generate_token(user_id):
  payload = {
    "sub": str(user_id),
    "exp": datetime.datetime.utcnow() + timedelta(days=1)
  }
  
  token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
  return token