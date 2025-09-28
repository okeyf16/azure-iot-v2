import logging
import json
import os
import azure.functions as func

# No special imports are needed for the legacy SDK pattern
from azure.iot.hub import IoTHubRegistryManager

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
        method_name = body.get("commandName")
        payload = body.get("payload", {})

        if not device_id or not method_name:
            return func.HttpResponse(
                json.dumps({"error": "deviceId and commandName are required"}),
                status_code=400,
                mimetype="application/json"
            )

        connection_string = os.getenv("IOTHUB_CONNECTION")
        if not connection_string:
            logging.error("IOTHUB_CONNECTION not set") 
            return func.HttpResponse(
                json.dumps({"error": "Server configuration error"}),
                status_code=500,
                mimetype="application/json"
            )

        registry_manager = IoTHubRegistryManager.from_connection_string(connection_string)
        
        # THIS IS THE KEY CHANGE FOR THE LEGACY SDK
        # The method name and payload must be in a single dictionary.
        method_payload = {
            "methodName": method_name,
            "payload": payload
            # Note: Timeout is not passed here in this version
        }
        
        # The function now receives the correct number of arguments:
        # 1. self (implicit)
        # 2. device_id
        # 3. method_payload
        response = registry_manager.invoke_device_method(device_id, method_payload)

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
        logging.exception("An unexpected error occurred while sending command")
        return func.HttpResponse(
            json.dumps({
                "status": "failed",
                "error": str(e)
            }),
            status_code=500,
            mimetype="application/json"
        )
