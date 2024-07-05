from flask import Blueprint, current_app
import os
import glob
from config import Config  # this is probably a bad way of doing things

bp = Blueprint('study', __name__, static_folder='static', static_url_path='/study_static')

from app.study import routes
