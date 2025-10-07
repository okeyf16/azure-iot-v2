import logging
import json
import os
import azure.functions as func

# Import the official Azure IoT Hub SDK classes with the DEFINITIVELY CORRECT import paths
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod
from azure.core.exceptions import HttpResponseError

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Device command function triggered (SDK - Final).")

    device_id = req.route_params.get('deviceId')
    
    if not device_id:
        return func.HttpResponse(
            json.dumps({"error": "deviceId must be provided in the URL"}),
            status_code=400,
            mimetype="application/json"
        )

    try:
        # Get the request body
        try:
            body = req.get_json()
        except ValueError:
            return func.HttpResponse(
                json.dumps({"error": "Invalid JSON body"}),
                status_code=400,
                mimetype="application/json"
            )

        method_name = body.get("commandName")
        payload = body.get("payload", {})

        if not method_name:
            return func.HttpResponse(
                json.dumps({"error": "commandName is required"}),
                status_code=400,
                mimetype="application/json"
            )

        # Get the connection string from application settings
        connection_string = os.getenv("IOTHUB_CONNECTION")
        if not connection_string:
            logging.error("IOTHUB_CONNECTION not set")
            return func.HttpResponse(
                json.dumps({"error": "Server configuration error"}),
                status_code=500,
                mimetype="application/json"
            )

        logging.info(f"Invoking method '{method_name}' on device '{device_id}'.")

        # Create an IoT Hub client from the connection string
        registry_manager = IoTHubRegistryManager.from_connection_string(connection_string)

        # Create the direct method payload using the correctly imported class
        device_method = CloudToDeviceMethod(method_name=method_name, payload=payload, response_timeout_in_seconds=30)

        # Invoke the method on the device
        result = registry_manager.invoke_device_method(device_id, device_method)

        logging.info(f"Successfully invoked method. Device responded with status: {result.status}")
        
        # Return the successful response from the device
        return func.HttpResponse(
            body=json.dumps(result.payload),
            status_code=result.status,
            mimetype="application/json"
        )

    except HttpResponseError as e:
        # This will catch errors from IoT Hub, such as 404 if the device is offline
        logging.error(f"IoT Hub returned an error: {e.reason}. Status: {e.status_code}", exc_info=True)
        error_details = {
            "error": "Failed to invoke device method via IoT Hub.",
            "details": e.reason,
            "status_code": e.status_code
        }
        return func.HttpResponse(
            body=json.dumps(error_details),
            status_code=e.status_code,
            mimetype="application/json"
        )
        
    except Exception as e:
        # This will catch any other unexpected errors
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)
        error_details = { "error": "An internal server error occurred.", "details": str(e) }
        return func.HttpResponse(
            body=json.dumps(error_details),
            status_code=500,
            mimetype="application/json"
        )
