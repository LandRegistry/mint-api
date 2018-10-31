from flask import Flask, g, request
import uuid
import requests
from mint_api.exceptions import ApplicationError
from jwt_validation.validate import validate
from jwt_validation.exceptions import ValidationFailure

app = Flask(__name__)

app.config.from_pyfile("config.py")


@app.before_request
def before_request():
    # Sets the transaction trace id into the global object if it has been provided in the HTTP header from the caller.
    # Generate a new one if it has not. We will use this in log messages.
    trace_id = request.headers.get('X-Trace-ID', None)
    if trace_id is None:
        trace_id = uuid.uuid4().hex
    g.trace_id = trace_id

    # We also create a session-level requests object for the app to use with the header pre-set, so other APIs will
    # receive it. These lines can be removed if the app will not make requests to other LR APIs!
    g.requests = requests.Session()
    g.requests.headers.update({'X-Trace-ID': trace_id})

    if '/health' in request.path:
        return

    if 'Authorization' not in request.headers:
        raise ApplicationError("Missing Authorization header", "AUTH1", 401)

    try:
        validate(app.config['AUTHENTICATION_API_URL'] + '/authentication/validate',
                 request.headers['Authorization'], g.requests)
    except ValidationFailure as fail:
        raise ApplicationError(fail.message, "AUTH1", 401)

    bearer_jwt = request.headers['Authorization']
    g.requests.headers.update({'Authorization': bearer_jwt})


@app.after_request
def after_request(response):
    # Add the API version (as in the interface spec, not the app) to the header. Semantic versioning applies - see the
    # API manual. A major version update will need to go in the URL. All changes should be documented though, for
    # reusing teams to take advantage of.
    response.headers["X-API-Version"] = "1.0.0"
    return response
