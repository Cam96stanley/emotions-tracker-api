import os

class DevelopmentConfig:
  SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
  SECRET_KEY = os.getenv("SECRET_KEY")
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  CACHE_TYPE = "SimpleCache"
  
class TestingConfig:
  SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
  SECRET_KEY = "super-secret-testing-key"
  DEBUG = True
  CACHE_TYPE = "SimpleCache"