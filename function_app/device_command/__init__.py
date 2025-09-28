import logging
import json
import azure.functions as func
from azure.iot.hub import IoTHubRegistryManager
import os
# Forcing a clean build v2

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Device command function triggered.")

    try:
        # Parse request JSON safely
        try:
            body = req.get_json()
        except ValueError:
            return func.HttpResponse(
                json.dumps({"error": "Invalid JSON body"}),
                status_code=400,
                mimetype="application/json"
            )

        device_id = body.get("deviceId")
        method_name = body.get("commandName", "turnOnOff")
        payload = body.get("payload", {})
        timeout = body.get("timeout", 30)

        if not device_id:
            return func.HttpResponse(
                json.dumps({"error": "deviceId is required"}),
                status_code=400,
                mimetype="application/json"
            )

        # Get IoT Hub connection string from environment
        connection_string = os.getenv("IOTHUB_CONNECTION")
        if not connection_string:
            return func.HttpResponse(
                json.dumps({"error": "IOTHUB_CONNECTION not set"}),
                status_code=500,
                mimetype="application/json"
            )

        # Connect to IoT Hub
        registry_manager = IoTHubRegistryManager(connection_string)

        # Create the direct method request object
        direct_method_request = DirectMethodRequest(
            method_name=method_name,
            payload=payload,
            response_timeout_in_seconds=timeout
        )
        
        # Invoke direct method on device
        response = registry_manager.invoke_device_method(
            device_id, direct_method_request
        )

        # Return IoT Hub response back to caller
        return func.HttpResponse(
            json.dumps({
                "status": "success",
                "deviceId": device_id,
                "methodResponse": response.as_dict()
            }),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        # Logs full traceback to App Insights
        logging.exception("Error sending command")
        return func.HttpResponse(
            json.dumps({
                "status": "failed",
                "error": str(e)
            }),
            status_code=500,
            mimetype="application/json"
        )
