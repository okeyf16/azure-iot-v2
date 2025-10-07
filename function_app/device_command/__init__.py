import logging
import json
import os
import azure.functions as func

# Import the official Azure IoT Hub SDK
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Device command function triggered (SDK).")

    device_id = req.route_params.get('deviceId')
    
    if not device_id:
        return func.HttpResponse(
            json.dumps({"error": "deviceId must be provided in the URL"}),
            status_code=400,
            mimetype="application/json"
        )

    try:
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

        connection_string = os.getenv("IOTHUB_CONNECTION")
        if not connection_string:
            logging.error("IOTHUB_CONNECTION not set")
            return func.HttpResponse(
                json.dumps({"error": "Server configuration error"}),
                status_code=500,
                mimetype="application/json"
            )

        # The SDK handles everything from here
        logging.info(f"Invoking method '{method_name}' on device '{device_id}' using SDK.")

        # 1. Create a client from the connection string. The SDK handles all parsing and auth.
        registry_manager = IoTHubRegistryManager.from_connection_string(connection_string)

        # 2. Create the direct method payload
        device_method = CloudToDeviceMethod(method_name=method_name, payload=payload)

        # 3. Invoke the method. The SDK builds the request, creates the SAS token, and makes the call.
        result = registry_manager.invoke_device_method(device_id, device_method)

        logging.info(f"Successfully invoked method. Device responded with status: {result.status}")
        
        # 4. Return the successful response from the device
        return func.HttpResponse(
            body=json.dumps(result.payload),
            status_code=result.status,
            mimetype="application/json"
        )

    except Exception as e:
        # The SDK will raise specific exceptions, which we can log.
        logging.error(f"An unexpected error occurred: {e}", exc_info=True)
        # Attempt to create a more helpful error message
        error_details = { "error": "Failed to invoke device method.", "details": str(e) }
        return func.HttpResponse(
            body=json.dumps(error_details),
            status_code=500, # Internal Server Error for failures
            mimetype="application/json"
        )
