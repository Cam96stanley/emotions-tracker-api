from flask import Blueprint

feeling_bp = Blueprint("feeling_bp", __name__)

from . import routes