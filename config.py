import os

class DevelopmentConfig:
  SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
  SECRET_KEY = os.getenv("SECRET_KEY") or "super secret key"
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  CACHE_TYPE = "SimpleCache"
  
class TestingConfig:
  SQLALCHEMY_DATABASE_URI = "sqlite:///testing.db"
  SECRET_KEY = "super-secret-testing-key"
  DEBUG = True
  CACHE_TYPE = "SimpleCache"
  
class ProductionConfig:
  PROD_SQLALCHEMY_DATABASE_URI = os.environ.get("PROD_SQLALCHEMY_DATABASE_URI")
  CACHE_TYPE = "SimpleCache"