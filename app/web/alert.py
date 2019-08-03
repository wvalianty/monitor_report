from . import web
from flask import abort, request, jsonify
from app.lib.environment import get_dingding_url
from app.view_models.message import Message
import requests, json


def report(msg, dingding_url, atmobiles=[], is_at_all="false"):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    post_data = {
        "msgtype": "text",
        "text": {
            "content": msg
        },
        "at": {
            "atMobiles": [str(phone) for phone in atmobiles],
            "isAtAll": is_at_all
        }
    }
    requests.post(dingding_url, headers=headers, data=json.dumps(post_data))


@web.route("/serverMonitorAlert", methods=["POST", "GET"])
def server():
    token = request.args.get("token")
    if token != "abc":
        abort(401)
    data = request.get_data()
    if len(data) < 3:
        abort(401)

    dingding_url = get_dingding_url("serverMonitorAlert")
    msg = Message(data).product()

    if len(msg) > 10:
        report(msg,dingding_url=dingding_url)
        return jsonify(m="yes")
    return jsonify(m="no")



@web.route("/fastsmsProjectProcess", methods=["POST", "GET"])
def fastsms():
    token = request.args.get("token")
    if token != "abc":
        abort(401)

    data = request.get_data()
    if len(data) < 3:
        abort(401)

    dingding_url = get_dingding_url("fastsmsProjectProcess")
    msg = Message(data).product()
    if len(msg) > 10:
        report(msg,dingding_url=dingding_url)
        return jsonify(m="yes")
    return jsonify(m="no")