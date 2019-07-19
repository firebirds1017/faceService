from flask import Blueprint

face = Blueprint('face', __name__)

from . import views, errors
