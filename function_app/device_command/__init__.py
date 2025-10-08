import logging
import json
import os
import azure.functions as func
import requests
from azure.identity import ManagedIdentityCredential

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Device command function triggered (Managed Identity).")

    device_id = req.route_params.get('deviceId')
    if not device_id:
        return func.HttpResponse(
            '{"error": "deviceId must be provided in the URL"}',
            status_code=400,
            mimetype="application/json"
        )

    try:
        # Get IoT Hub hostname (e.g., myhub.azure-devices.net)
        hostname = os.getenv("IOTHUB_HOSTNAME")
        if not hostname:
            logging.error("IOTHUB_HOSTNAME application setting is not set.")
            return func.HttpResponse(
                '{"error": "Server configuration error"}',
                status_code=500,
                mimetype="application/json"
            )

        # Parse incoming request
        req_body = req.get_json()
        method_name = req_body.get("commandName")
        payload = req_body.get("payload", {})

        if not method_name:
            return func.HttpResponse(
                '{"error": "commandName is required"}',
                status_code=400,
                mimetype="application/json"
            )

        logging.info(f"Authenticating with Managed Identity to invoke '{method_name}' on device '{device_id}'.")

        # 1. Get an access token for IoT Hub using Managed Identity
        credential = ManagedIdentityCredential()
        # Note the scope for service-level APIs
        token_info = credential.get_token("https://iothubs.azure.net/.default")
        token = token_info.token

        # 2. Construct the REST API URL for invoking a direct method
        api_version = "2021-04-12"
        rest_api_url = f"https://{hostname}/twins/{device_id}/methods?api-version={api_version}"

        # 3. Prepare the request headers and body
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        body = {
            "methodName": method_name,
            "payload": payload,
            "responseTimeoutInSeconds": 30
        }

        logging.info(f"Invoking method '{method_name}' on device '{device_id}' via REST API...")
        
        # 4. Make the POST request
        response = requests.post(rest_api_url, headers=headers, json=body)
        response.raise_for_status()  # This will raise an exception for HTTP error codes (4xx or 5xx)

        response_json = response.json()
        logging.info(f"Device method invoked successfully. Response: {response_json}")
        
        return func.HttpResponse(
            json.dumps(response_json),
            status_code=response.status_code,
            mimetype="application/json"
        )

    except requests.exceptions.HTTPError as hre:
        logging.error(f"HTTP error from IoT Hub REST API: {hre.response.text}", exc_info=True)
        return func.HttpResponse(
            json.dumps({"error": "IoT Hub returned an error", "details": hre.response.json()}),
            status_code=hre.response.status_code
        )
    except Exception as e:
        logging.error(f"An internal error occurred: {e}", exc_info=True)
        return func.HttpResponse(
            json.dumps({"error": "Internal error", "details": str(e)}),
            status_code=500
        )
