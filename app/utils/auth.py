from flask_bcrypt import Bcrypt
from functools import wraps
from jose import jwt
import datetime
from datetime import timedelta
from flask import current_app, jsonify, request
import jose

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

def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    print("Decorator running")
    token = None
    
    if "Authorization" in request.headers:
        print("Authorization header:", request.headers["Authorization"])
        token = request.headers["Authorization"].split(" ")[1]
      
    if not token:
      print("Token not found")
      return jsonify({"message": "Token is missing"}), 401
    
    try:
      data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
      user_id = data["sub"]
      
    except jose.exceptions.ExpiredSignatureError:
      print("Token Expired")
      return jsonify({"message": "Token has expired!"}), 401
    
    except jose.exceptions.JWTError:
      print("Token invalid")
      return jsonify({"message": "Invalid token!"}), 401
    
    print("Token valid for user:", user_id)
    return f(user_id, *args, **kwargs)
  return decorated