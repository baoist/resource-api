from functools import wraps
from flask import (g, request, Response, redirect,
                  url_for, Flask, jsonify, json)
from flask.ext.httpauth import HTTPBasicAuth
from models.base import db
from models.user import User
from models.cyclopedia import Cyclopedia
from models.entry import Entry
from services.cyclopedia_service import CyclopediaService
from presenters.cyclopedia_presenter import CyclopediaPresenter
from authentication.verification import Authenticator

import config

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.auth = HTTPBasicAuth()
db.init_app(app)


def require_apikey(fn):
    @wraps(fn)
    def _wrap(*args, **kwargs):
        auth = request.authorization
        authenticator = Authenticator(auth.username)
        user = authenticator.authenticate()

        if not auth.username or not user:
            return Response(response='401 Unauthorized.',
                        status=401,
                        mimetype="application/json")

        g.user = user
        return fn(*args, **kwargs)
    return _wrap


@app.route("/api/users/create", methods=["POST"])
def create_user():
    auth = request.authorization
    user = User(auth.username, auth.password)

    db.session.add(user)
    if db.session.commit():
        return jsonify(user = user._asdict())
    else:
        return Response(response='400 Unable to create user.',
                        status=400,
                        mimetype="application/json")


@app.route("/api/log-in", methods=["POST"])
def login():
    auth = request.authorization

    authenticator = Authenticator(auth.username, auth.password)
    user = authenticator.authenticate()

    if user:
        g.user = user
        return jsonify(user = user._asdict())
    else:
        return Response(response='401 Unauthorized.',
                        status=401,
                        mimetype="application/json")


@app.route("/api/cyclopedias/create", methods=["POST"])
@require_apikey
def create_cyclopedia():
    cyclopedia_params = request.get_json(force=True)

    if cyclopedia_params.get('topic', False):
        cyclopedia_service = CyclopediaService()
        cyclopedia = cyclopedia_service.create(cyclopedia_params.get('topic'),
                                               g.user,
                                               cyclopedia_params.get('parents', ""))

        if cyclopedia:
            presenter = CyclopediaPresenter()
            presenter.dump(cyclopedia)

            return jsonify(cyclopedia = cyclopedia._asdict())

    return Response(response='400 Unable to create cyclopedia.',
                    status=400,
                    mimetype="application/json")


@app.route("/api/cyclopedias", methods=["GET"])
@require_apikey
def get_cyclopedia():
    cyclopedia_params = request.get_json(force=True)

    cyclopedia_service = CyclopediaService()

    if cyclopedia_params.get('topics', False):
        return Response(response='400 Unable to create cyclopedia.',
                    status=400,
                    mimetype="application/json")
    else:
        cyclopedias = cyclopedia_service.get_root_cyclopedias(g.user.id)

        cyclopedias_presenter = CyclopediaPresenter(many=True)
        cyclopedias_result = cyclopedias_presenter.dump(cyclopedias)

        return jsonify(cyclopedias = cyclopedias_result.data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
