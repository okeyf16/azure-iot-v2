import logging
import json
import os
import requests
import time
import hmac
import hashlib
import base64
from urllib.parse import quote_plus, urlencode

import azure.functions as func

# Helper function to generate the necessary security token (No changes needed here)
def generate_sas_token(uri, key, policy_name, expiry=3600):
    ttl = time.time() + expiry
    sign_key = "%s\n%d" % ((quote_plus(uri)), int(ttl))
    signature = base64.b64encode(hmac.new(base64.b64decode(key), sign_key.encode('utf-8'), hashlib.sha256).digest())

    raw_token = {
        'sr': uri,
        'sig': signature,
        'se': str(int(ttl))
    }

    if policy_name is not None:
        raw_token['skn'] = policy_name

    return 'SharedAccessSignature ' + urlencode(raw_token)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Device command function triggered (REST API).")

    # --- CHANGE #1: Get device_id from the URL route parameters ---
    device_id = req.route_params.get('deviceId')
    
    if not device_id:
        return func.HttpResponse(json.dumps({"error": "deviceId must be provided in the URL path, e.g., /api/command/my-device"}), status_code=400, mimetype="application/json")

    try:
        # Parse request JSON safely
        try:
            body = req.get_json()
        except ValueError:
            return func.HttpResponse(json.dumps({"error": "Invalid JSON body"}), status_code=400, mimetype="application/json")

        # --- CHANGE #2: We no longer get device_id from the body ---
        method_name = body.get("commandName")
        payload = body.get("payload", {})
        timeout = body.get("timeout", 30)

        if not method_name:
            return func.HttpResponse(json.dumps({"error": "commandName is required in the JSON body"}), status_code=400, mimetype="application/json")

        connection_string = os.getenv("IOTHUB_CONNECTION")
        if not connection_string:
            logging.error("IOTHUB_CONNECTION not set")
            return func.HttpResponse(json.dumps({"error": "Server configuration error"}), status_code=500, mimetype="application/json")

        # Parse the connection string (no changes here)
        parts = {p[0]: p[1] for p in [s.split('=', 1) for s in connection_string.split(';')]}
        hostname = parts.get("HostName")
        policy_name = parts.get("SharedAccessKeyName")
        key = parts.get("SharedAccessKey")

        if not all([hostname, policy_name, key]):
             logging.error("Connection string is missing required parts (HostName, SharedAccessKeyName, SharedAccessKey)")
             return func.HttpResponse(json.dumps({"error": "Server configuration error"}), status_code=500, mimetype="application/json")

        # REST API LOGIC (no changes here)
        api_version = "2021-04-12"
        rest_api_url = f"https://{hostname}/twins/{device_id}/methods?api-version={api_version}"
        
        sas_token = generate_sas_token(hostname, key, policy_name)

        headers = {
            "Authorization": sas_token,
            "Content-Type": "application/json"
        }

        rest_api_body = {
            "methodName": method_name,
            "payload": payload,
            "responseTimeoutInSeconds": timeout
        }

        response = requests.post(rest_api_url, headers=headers, json=rest_api_body)
        response.raise_for_status()

        response_json = response.json()
        
        return func.HttpResponse(
            body=json.dumps(response_json),
            status_code=response_json.get("status", 200),
            mimetype="application/json"
        )

    except requests.exceptions.HTTPError as e:
        logging.exception("HTTP error occurred while calling IoT Hub REST API")
        error_body = e.response.text
        return func.HttpResponse(
            body=error_body,
            status_code=e.response.status_code,
            mimetype="application/json"
        )
    except Exception as e:
        logging.exception("An unexpected error occurred")
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, mimetype="application/json")
