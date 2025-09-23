import logging
import azure.functions as func
from azure.iot.hub import IoTHubRegistryManager
import os
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Received device command request.")

    try:
        device_id = req.route_params.get("device_id")
        body = req.get_json()

        iothub_connection = os.getenv("IOTHUB_CONNECTION")
        registry_manager = IoTHubRegistryManager(iothub_connection)

        # Example: invoke direct method "setOnOff"
        method_name = "setOnOff"
        payload = {"state": body.get("state", "off")}

        response = registry_manager.invoke_device_method(device_id, method_name, payload)
        logging.info(f"Command sent to {device_id}, response: {response}")

        return func.HttpResponse(json.dumps(response.as_dict()), status_code=200)

    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse(str(e), status_code=500)
