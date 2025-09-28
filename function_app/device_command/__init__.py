import logging
import json
import os
import azure.functions as func

# IMPORTING THE MODERN V2 CLIENT
from azure.iot.hub import IoTHubServiceClient

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
        timeout = body.get("timeout", 30)

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

        # USING THE MODERN V2 CLIENT
        service_client = IoTHubServiceClient.from_connection_string(connection_string)
        
        # The modern client has a clean, stable method signature
        response = service_client.invoke_device_method(
            device_id=device_id, 
            direct_method_request={
                "method_name": method_name,
                "payload": payload,
                "response_timeout_in_seconds": timeout
            }
        )

        # Always close the client when you're done
        service_client.shutdown()

        return func.HttpResponse(
            json.dumps({
                "status": "success",
                "deviceId": device_id,
                "methodResponse": response.payload
            }),
            status_code=response.status,
            mimetype="application/json"
        )

    except Exception as e:
        logging.exception("An unexpected error occurred while sending command")
        if 'service_client' in locals():
            service_client.shutdown() # Ensure client is shut down on error
        return func.HttpResponse(
            json.dumps({
                "status": "failed",
                "error": str(e)
            }),
            status_code=500,
            mimetype="application/json"
        )
