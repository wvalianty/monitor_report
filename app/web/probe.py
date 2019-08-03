from . import web
from flask import jsonify

@web.route("/probe")
def probe():
    return jsonify(a=1)