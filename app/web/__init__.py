from flask import Blueprint


web = Blueprint('web', __name__)


from app.web import alert
from app.web import probe