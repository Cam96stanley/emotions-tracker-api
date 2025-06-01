from flask import Blueprint

user_bp = Blueprint("user_bp", url_prefix="/users")

from . import routes