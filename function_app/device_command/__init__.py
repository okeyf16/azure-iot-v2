import logging
import json
import os
import requests
import azure.functions as func

# CHANGE 1: Import the specific ManagedIdentityCredential instead of the default
from azure.identity import ManagedIdentityCredential
from azure.core.exceptions import HttpResponseError

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Device command function triggered (Specific Managed Identity).")

    device_id = req.route_params.get('deviceId')
    
    if not device_id:
        return func.HttpResponse(json.dumps({"error": "deviceId must be provided in the URL"}), status_code=400)

    try:
        # Get the IoT Hub hostname from an application setting
        hostname = os.getenv("IOTHUB_HOSTNAME")
        if not hostname:
            logging.error("IOTHUB_HOSTNAME application setting is not set.")
            return func.HttpResponse(json.dumps({"error": "Server configuration error"}), status_code=500)

        # Get the incoming request body
        body = req.get_json()
        method_name = body.get("commandName")
        payload = body.get("payload", {})
        
        if not method_name:
            return func.HttpResponse(json.dumps({"error": "commandName is required"}), status_code=400)

        logging.info(f"Authenticating using specific Managed Identity to call '{method_name}' on '{device_id}'.")

        # CHANGE 2: Create an instance of ManagedIdentityCredential directly
        credential = ManagedIdentityCredential()

        # Get an OAuth 2.0 access token for the correct IoT Hub resource scope.
        token_info = credential.get_token("https://management.azure.net/.default")
        access_token = token_info.token

        # Prepare the REST API call
        api_version = "2021-04-12"
        rest_api_url = f"https://{hostname}/twins/{device_id}/methods?api-version={api_version}"
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        rest_api_body = {
            "methodName": method_name,
            "payload": payload,
            "responseTimeoutInSeconds": 30
        }

        # Make the authenticated request
        response = requests.post(rest_api_url, headers=headers, json=rest_api_body)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)

        logging.info(f"Successfully invoked method. Device responded with status: {response.status_code}")
        return func.HttpResponse(body=response.text, status_code=response.status_code, mimetype="application/json")

    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        return func.HttpResponse(json.dumps({"error": "An internal error occurred", "details": str(e)}), status_code=500)
