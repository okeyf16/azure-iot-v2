import logging
import json
import os
import requests
import time
import hmac
import hashlib
import base64
from urllib.parse import urlencode

import azure.functions as func

# --- MODIFIED: Corrected SAS Token Logic ---
def generate_sas_token(uri, key, policy_name, expiry=3600):
    """Generates a SAS token for Azure IoT Hub authentication."""
    ttl = int(time.time()) + expiry
    
    # The string-to-sign should be the URI followed by a newline and the expiry time.
    # The URI itself should NOT be URL-encoded for the signature calculation.
    string_to_sign = f"{uri}\n{ttl}"

    # Sign the string with the key
    signature = hmac.new(
        base64.b64decode(key),
        string_to_sign.encode('utf-8'),
        hashlib.sha256
    ).digest()
    
    # Base64 encode the signature
    encoded_signature = base64.b64encode(signature)

    # Construct the token as a dictionary
    token_data = {
        'sr': uri,
        'sig': encoded_signature,
        'se': str(ttl)
    }
    if policy_name:
        token_data['skn'] = policy_name

    # URL-encode the final token string
    return 'SharedAccessSignature ' + urlencode(token_data)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Device command function triggered (REST API).")

    device_id = req.route_params.get('deviceId')
    
    if not device_id:
        return func.HttpResponse(json.dumps({"error": "deviceId must be provided in the URL"}), status_code=400, mimetype="application/json")

    try:
        try:
            body = req.get_json()
        except ValueError:
            return func.HttpResponse(json.dumps({"error": "Invalid JSON body"}), status_code=400, mimetype="application/json")

        method_name = body.get("commandName")
        payload = body.get("payload", {})
        timeout = body.get("timeout", 30)

        if not method_name:
            return func.HttpResponse(json.dumps({"error": "commandName is required"}), status_code=400, mimetype="application/json")

        connection_string = os.getenv("IOTHUB_CONNECTION")
        if not connection_string:
            logging.error("IOTHUB_CONNECTION not set")
            return func.HttpResponse(json.dumps({"error": "Server configuration error"}), status_code=500, mimetype="application/json")

        parts = {p[0]: p[1] for p in [s.split('=', 1) for s in connection_string.split(';')]}
        hostname = parts.get("HostName")
        policy_name = parts.get("SharedAccessKeyName")
        key = parts.get("SharedAccessKey")

        if not all([hostname, policy_name, key]):
             logging.error("Connection string is missing required parts")
             return func.HttpResponse(json.dumps({"error": "Server configuration error"}), status_code=500, mimetype="application/json")

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

        return func.HttpResponse(
            body=json.dumps(response.json()),
            status_code=response.status_code,
            mimetype="application/json"
        )

    except requests.exceptions.HTTPError as e:
        logging.exception("HTTP error occurred while calling IoT Hub REST API")
        return func.HttpResponse(
            body=e.response.text,
            status_code=e.response.status_code,
            mimetype="application/json"
        )
    except Exception as e:
        logging.exception("An unexpected error occurred")
        return func.HttpResponse(json.dumps({"error": str(e)}), status_code=500, mimetype="application/json")
