from flask import Blueprint

usermood_bp = Blueprint("usermood_bp", __name__)

from . import routes