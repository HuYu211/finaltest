from flask import request,jsonify,Flask,Blueprint,Flask

route_getToken =Blueprint("getToken_page",__name__)

@route_getToken.route("/")
def index():
    return "test"