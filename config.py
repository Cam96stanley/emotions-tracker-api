import os

class DevelopmentConfig:
  SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:Cam.110196@localhost/emotion_tracker_db"
  SECRET_KEY = os.getenv("SECRET_KEY") or "super secret key"
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  CACHE_TYPE = "SimpleCache"
  
class TestingConfig:
  SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
  SECRET_KEY = "super-secret-testing-key"
  DEBUG = True
  CACHE_TYPE = "SimpleCache"
  
class ProductionConfig:
  SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
  CACHE_TYPE = "SimpleCache"
  SECRET_KEY = os.environ.get("SECRET_KEY")