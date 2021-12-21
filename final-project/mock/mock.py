#!/usr/bin/env python3.8

from flask import Flask, jsonify

app = Flask(__name__)

USER_ID_DATA = {"administrator": 1, "alexandra": 2, "robert": 3}


@app.route("/vk_id/<username>", methods=["GET"])
def get_user_surname(username):
    if user_id := USER_ID_DATA.get(username):
        return jsonify({"vk_id": str(user_id)}), 200
    else:
        return jsonify({}), 404


app.run(host="0.0.0.0", port=5000)
