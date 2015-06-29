from functools import wraps
from flask import (g, request, Response, Flask, jsonify)
from flask.ext.httpauth import HTTPBasicAuth
from models.base import db
from services.cyclopedia_service import CyclopediaService
from services.user_service import UserService
from services.entry_service import EntryService
from services.authentication_service import AuthenticationService
from presenters.user_presenter import UserPresenter
from presenters.cyclopedia_presenter import CyclopediaPresenter
from presenters.entry_presenter import EntryPresenter

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.auth = HTTPBasicAuth()
db.init_app(app)


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response('Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def require_apikey(fn):
    @wraps(fn)
    def _wrap(*args, **kwargs):
        auth = request.authorization

        if not auth:
            return authenticate()

        authenticator = AuthenticationService(auth.username)
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
    """
    Params a username:password (required) and attempts to create a user.

    Username is a unique field.
    """
    auth = request.authorization

    user_service = UserService()
    created_user = user_service.create(auth.username, auth.password)

    if created_user:
        user_presenter = UserPresenter()
        user_result = user_presenter.dump(created_user)

        return jsonify(user_result.data)

    return Response(response='400 Unable to create user. User already exists.',
                    status=400,
                    mimetype="application/json")


@app.route("/api/log-in", methods=["POST"])
def login():
    """
    Params a username:password and attempts to log in.
    """
    auth = request.authorization

    authenticator = AuthenticationService(auth.username, auth.password)
    user = authenticator.authenticate()

    if user:
        g.user = user

        user_presenter = UserPresenter()
        user_result = user_presenter.dump(user)

        return jsonify(user_result.data)
    else:
        return Response(response='401 Unauthorized.',
                        status=401,
                        mimetype="application/json")


@app.route("/api/cyclopedias/create", methods=["POST"])
@require_apikey
def create_cyclopedia():
    """
    Params:
    `topic` (required, string)
    `path` (optional, array)

    Attempts to create a cyclopedia.
    """
    cyclopedia_params = request.get_json(force=True)
    cyclopedia_service = CyclopediaService()

    if cyclopedia_params.get('topic', False):
        cyclopedia = cyclopedia_service.create(cyclopedia_params.get('topic'),
                                               g.user,
                                               cyclopedia_params.get('path', ""))

        if cyclopedia:
            cyclopedia_presenter = CyclopediaPresenter()
            cyclopedia_result = cyclopedia_presenter.dump(cyclopedia)

            return jsonify(cyclopedia_result.data)

    return Response(response='400 Unable to create cyclopedia.',
                    status=400,
                    mimetype="application/json")


@app.route("/api/cyclopedias", methods=["GET"])
@require_apikey
def get_cyclopedia():
    """
    Params:
    `path` (optional, array)

    Retrieves the tree of cyclopedias and entries.
    If a `path` is passed the subtree beginning at that descendent.
    """
    cyclopedia_params = request.get_json(force=True, silent=True)

    cyclopedia_service = CyclopediaService()

    if cyclopedia_params and cyclopedia_params.get('path', False):
        node_topic_id = cyclopedia_service.get_parent_node_id(cyclopedia_params.get('path'))
        cyclopedia = cyclopedia_service.find(node_topic_id)

        cyclopedias_presenter = CyclopediaPresenter()
        cyclopedias_result = cyclopedias_presenter.dump(cyclopedia)

        return jsonify(cyclopedias_result.data)
    else:
        cyclopedia = cyclopedia_service.get_root_cyclopedia(g.user.id)

        cyclopedias_presenter = CyclopediaPresenter()
        cyclopedias_result = cyclopedias_presenter.dump(cyclopedia)

        return jsonify(cyclopedias_result.data)


@app.route("/api/entries/create", methods=["POST"])
@require_apikey
def create_entry():
    """
    Params:
    `term` (required, string)
    `title` (optional, string)
    `image_url` (optional, string)
    `description` (optional, string)
    `path` (optional, array)

    Attempts to create an entry. Path indicates tree of cyclopedias.
    """
    entry_params = request.get_json(force=True)

    if entry_params.get('term', False):
        entry_service = EntryService()
        entry = entry_service.create(entry_params.get('term'),
                                     g.user,
                                     entry_params.get('title', entry_params.get('term')),
                                     entry_params.get('image_url', None),
                                     entry_params.get('description', None),
                                     entry_params.get('path', None))

        if entry:
            entry_presenter = EntryPresenter()
            entry_result = entry_presenter.dump(entry)

            return jsonify(entry_result.data)

    return Response(response='400 Unable to create entry.',
                    status=400,
                    mimetype="application/json")


@app.route("/api/entries/<path:entry_id>", methods=["GET"])
@require_apikey
def get_entry(entry_id):
    entry_service = EntryService()
    entry = entry_service.find(g.user.id, entry_id)

    if entry:
        entry_presenter = EntryPresenter()
        entry_result = entry_presenter.dump(entry)

        return jsonify(entry_result.data)

    return Response(response='400 Unable to find entry.',
                    status=400,
                    mimetype="application/json")


@app.route("/api/entries/<path:entryid>", methods=["DELETE"])
@require_apikey
def delete_entry(entryid):
    entry_service = EntryService()
    entry = entry_service.find(g.user.id, entryid)

    if entry:
        entry_service.destroy(entry)

        return Response(response='200 Successfully deleted entry %s.' % entry.id,
                        status=200,
                        mimetype="application/json")

    return Response(response='400 Unable to find entry.',
                    status=400,
                    mimetype="application/json")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
