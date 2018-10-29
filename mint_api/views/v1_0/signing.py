import json
from flask import current_app, g
from flask import request, Blueprint, Response
from mint_api.exceptions import ApplicationError
from mint_api.extensions import crypto
from mint_api.utilities.charge_id import ChargeIdService

# This is the blueprint object that gets registered into the app in blueprints.py.
signing = Blueprint('signing', __name__)


@signing.route("/records", methods=["POST"])
def sign_send():
    current_app.logger.info("Endpoint called")
    register_id = current_app.config['IDENTIFIER_KEY']
    item = request.get_json()
    if not item:
        current_app.logger.warning("Received non-JSON POST request.")
        raise ApplicationError("POST request must contain JSON", "E102", 400)
    if register_id not in item:
        current_app.logger.info("Generating Charge ID")
        item[register_id] = ChargeIdService.generate_charge_id()
    current_app.logger.info("Using Charge ID: %s", item[register_id])
    payload = json.dumps(item, sort_keys=True, separators=(',', ':'))
    signature, payload_hash = crypto.sign_payload(payload)
    post_payload = {"item": item, "item-hash": payload_hash, "item-signature": signature}
    current_app.audit_logger.info("Item for register '{0}' signed, sending to SOR.".format(item[register_id]))
    res = g.requests.post("{0}/record".format(current_app.config["SOR_URL"]),
                          data=json.dumps(post_payload, sort_keys=True, separators=(',', ':')),
                          headers={"Content-Type": "application/json"})

    if res.status_code == 400:
        current_app.logger.warning(
            "POST to register failed with status {:d}, response was: {}".format(res.status_code, res.json()))
        result = res.json()
    elif res.status_code == 202:
        current_app.logger.info("Item for register '{0}' sent to SOR.".format(item[register_id]))
        result = res.json()
        result.update({
            register_id: item[register_id]
        })
    else:
        current_app.logger.warning(
            "POST to register failed with status {:d}, response was: {}".format(res.status_code, res.text))
        return res

    current_app.logger.info("Return results with status code: %d", res.status_code)
    return Response(json.dumps(result), mimetype='application/json', status=res.status_code)
