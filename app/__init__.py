import os
from flask import Flask
from app.models import db
from app.extensions import ma
from app.blueprints.user import user_bp
from app.utils.auth import bcrypt

def create_app(config_name):
  app = Flask(__name__)
  app.config.from_object(f"config.{config_name}")
  UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
  os.makedirs(UPLOAD_FOLDER, exist_ok=True)
  
  app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
  app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
  
  db.init_app(app)
  ma.init_app(app)
  bcrypt.init_app(app)
  
  app.register_blueprint(user_bp)
  
  return app