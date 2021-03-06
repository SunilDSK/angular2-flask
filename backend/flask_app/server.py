"""Entry point for the server application."""

import json
import logging
import traceback

from flask import Response, request
from flask_security import auth_token_required, utils
from gevent.wsgi import WSGIServer

from .app_utils import html_codes, token_login
from .factory import create_app, create_user

logger = logging.getLogger(__name__)
app = create_app()


@app.before_first_request
def init():
    """Initialize the application with defaults."""
    create_user(app)


@app.route("/api/logoutuser", methods=['POST'])
@auth_token_required
def logout():
    """Logout the currently logged in user."""
    logger.info('Logged out user !!')
    utils.logout_user()
    return 'logged out successfully', 200


@app.route('/api/loginuser', methods=['POST'])
def login():
    """View function for login view."""
    logger.info('Logged in user')
    return token_login.login_with_token(request, app)


@app.route('/api/getdata', methods=['POST'])
@auth_token_required
def get_data():
    """Get dummy data returned from the server."""
    data = {'Heroes': ['Hero1', 'Hero2', 'Hero3']}
    json_response = json.dumps(data)
    return Response(json_response,
                    status=html_codes.HTTP_OK_BASIC,
                    mimetype='application/json')


def main():
    """Main entry point of the app."""
    try:
        port = 8080
        ip = '0.0.0.0'
        http_server = WSGIServer((ip, port),
                                 app,
                                 log=logging,
                                 error_log=logging)
        print("Server started at: {0}:{1}".format(ip, port))
        http_server.serve_forever()
    except Exception as exc:
        logger.error(exc.message)
        logger.exception(traceback.format_exc())
    finally:
        # Do something here
        pass
