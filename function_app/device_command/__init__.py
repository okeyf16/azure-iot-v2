import logging
import json
import os
import azure.functions as func
from azure.identity import ManagedIdentityCredential
from azure.iot.hub import IoTHubRegistryManager
from azure.core.exceptions import HttpResponseError


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Device command function triggered (Managed Identity).")

    device_id = req.route_params.get('deviceId')
    if not device_id:
        return func.HttpResponse(
            json.dumps({"error": "deviceId must be provided in the URL"}),
            status_code=400
        )

    try:
        # Get IoT Hub hostname (e.g., myhub.azure-devices.net)
        hostname = os.getenv("IOTHUB_HOSTNAME")
        if not hostname:
            logging.error("IOTHUB_HOSTNAME application setting is not set.")
            return func.HttpResponse(
                json.dumps({"error": "Server configuration error"}),
                status_code=500
            )

        # Parse incoming request
        body = req.get_json()
        method_name = body.get("commandName")
        payload = body.get("payload", {})

        if not method_name:
            return func.HttpResponse(
                json.dumps({"error": "commandName is required"}),
                status_code=400
            )

        logging.info(f"Authenticating with Managed Identity to invoke '{method_name}' on device '{device_id}'.")

        # ✅ Use Managed Identity to authenticate with IoT Hub
        credential = ManagedIdentityCredential()
        token = credential.get_token("https://iothubs.azure.net/.default").token

        # Initialize RegistryManager using token directly
        registry_manager = IoTHubRegistryManager.from_token(hostname, token)

        # Build method payload
        direct_method = {
            "methodName": method_name,
            "payload": payload,
            "responseTimeoutInSeconds": 30
        }

        logging.info(f"Invoking method {method_name} on device {device_id}...")
        response = registry_manager.invoke_device_method(device_id, direct_method)

        logging.info(f"Device method invoked successfully. Response: {response}")
        return func.HttpResponse(
            json.dumps({
                "status": response.status,
                "payload": response.payload
            }),
            status_code=200,
            mimetype="application/json"
        )

    except HttpResponseError as hre:
        logging.error(f"HTTP error from IoT Hub: {hre}", exc_info=True)
        return func.HttpResponse(
            json.dumps({"error": "IoT Hub returned an error", "details": str(hre)}),
            status_code=hre.status_code if hasattr(hre, "status_code") else 500
        )
    except Exception as e:
        logging.error(f"An internal error occurred: {e}", exc_info=True)
        return func.HttpResponse(
            json.dumps({"error": "Internal error", "details": str(e)}),
            status_code=500
        )
