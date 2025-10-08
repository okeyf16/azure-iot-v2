import logging
import json
import os
import requests
import azure.functions as func

from azure.identity import ManagedIdentityCredential
from azure.core.exceptions import ClientAuthenticationError, HttpResponseError

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Device command function triggered (Managed Identity).")

    device_id = req.route_params.get('deviceId')
    
    if not device_id:
        return func.HttpResponse(json.dumps({"error": "deviceId must be provided in the URL"}), status_code=400)

    try:
        hostname = os.getenv("IOTHUB_HOSTNAME")
        if not hostname:
            logging.error("IOTHUB_HOSTNAME application setting is not set.")
            return func.HttpResponse(json.dumps({"error": "Server configuration error"}), status_code=500)

        body = req.get_json()
        method_name = body.get("commandName")
        payload = body.get("payload", {})
        
        if not method_name:
            return func.HttpResponse(json.dumps({"error": "commandName is required"}), status_code=400)

        logging.info(f"Authenticating with Managed Identity to invoke '{method_name}' on device '{device_id}'.")

        # 1. Get a credential object for the function's Managed Identity.
        credential = ManagedIdentityCredential()

        # 2. Get an OAuth 2.0 access token for the CORRECT IoT Hub data service.
        token_info = credential.get_token("https://devices.azure.net/.default")
        access_token = token_info.token
        logging.info("Successfully acquired authentication token.")

        # 3. Prepare the REST API call.
        api_version = "2021-04-12"
        rest_api_url = f"https://{hostname}/twins/{device_id}/methods?api-version={api_version}"
        
        # 4. Use the token in the "Authorization" header.
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        rest_api_body = {
            "methodName": method_name,
            "payload": payload,
            "responseTimeoutInSeconds": 30
        }

        # 5. Make the authenticated request.
        response = requests.post(rest_api_url, headers=headers, json=rest_api_body)
        response.raise_for_status()

        logging.info(f"Successfully invoked method. Device responded with status: {response.status_code}")
        return func.HttpResponse(body=response.text, status_code=response.status_code, mimetype="application/json")

    except ClientAuthenticationError as e:
        logging.error(f"Authentication failed: {e}", exc_info=True)
        return func.HttpResponse(json.dumps({"error": "Authentication failed", "details": str(e)}), status_code=500)

    except requests.exceptions.HTTPError as e:
        logging.error(f"IoT Hub returned an HTTP error: {e.response.text}", exc_info=True)
        return func.HttpResponse(body=e.response.text, status_code=e.response.status_code, mimetype="application/json")
        
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)
        return func.HttpResponse(json.dumps({"error": "An internal error occurred", "details": str(e)}), status_code=500)
