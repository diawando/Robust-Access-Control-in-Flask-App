from flask import Blueprint, jsonify

blog = Blueprint("views", __name__)

@blog.get("/")
def status():
    return jsonify({
        "status" : "Up and running"
    }), 200