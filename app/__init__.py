import os
from flask import Flask
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from app.models import db
from app.extensions import ma
from app.blueprints.user import user_bp
from app.blueprints.feeling import feeling_bp
from app.blueprints.usermood import usermood_bp
from app.utils.auth import bcrypt

SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.yaml"

swaggerui_blueprint = get_swaggerui_blueprint(
  SWAGGER_URL,
  API_URL,
  config = {
    "app_name": "Emotion Tracker API"
  }
)

def create_app(config_name):
  app = Flask(__name__)
  CORS(app)
  app.config.from_object(f"config.{config_name}")
  
  UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
  os.makedirs(UPLOAD_FOLDER, exist_ok=True)
  
  app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
  app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
  
  db.init_app(app)
  ma.init_app(app)
  bcrypt.init_app(app)
  
  app.register_blueprint(user_bp, url_prefix="/users")
  app.register_blueprint(feeling_bp, url_prefix="/feelings")
  app.register_blueprint(usermood_bp, url_prefix="/usermoods")
  app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
  
  return app