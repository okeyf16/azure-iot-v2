import logging
import json
import os
import azure.functions as func

# The DirectMethodRequest class is not needed with the modern SDK
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
        method_name = body.get("commandName") # Get the method name from the request
        payload = body.get("payload", {})
        timeout = body.get("timeout", 30)

        if not device_id or not method_name:
            return func.HttpResponse(
                json.dumps({"error": "deviceId and commandName are required"}),
                status_code=400,
                mimetype="application/json"
            )

        # Get IoT Hub connection string from environment
        connection_string = os.getenv("IOTHUB_CONNECTION")
        if not connection_string:
            # This error is for server configuration issues
            logging.error("IOTHUB_CONNECTION not set") 
            return func.HttpResponse(
                json.dumps({"error": "Server configuration error"}),
                status_code=500,
                mimetype="application/json"
            )

        # Connect to IoT Hub using the recommended class method
        registry_manager = IoTHubRegistryManager.from_connection_string(connection_string)
        
        # SIMPLIFIED: Invoke the method directly with its name and payload
        response = registry_manager.invoke_device_method(
            device_id, method_name, payload
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
        # Logs full traceback to App Insights for better debugging
        logging.exception("An unexpected error occurred while sending command")
        return func.HttpResponse(
            json.dumps({
                "status": "failed",
                "error": str(e)
            }),
            status_code=500,
            mimetype="application/json"
        )
