# Assuming your function is in: /home/site/wwwroot/device_command/__init__.py

import logging
import json
import os
from azure.iot.hub import IoTHubRegistryManager
# 💡 IMPORT THE NECESSARY MODEL from the SDK
from azure.iot.hub.models import CloudToDeviceMethod 

# --- Configuration ---
# Get your IoT Hub connection string from environment variables
IOT_HUB_CONN_STR = os.environ.get("AzureWebJobsIoTHubConnectionString") 
DEVICE_ID = "SimDevice01"  # Replace with the actual device ID

# Initialize the Registry Manager outside the main function for better performance
try:
    # This assumes you have the IOT_HUB_CONN_STR set up
    registry_manager = IoTHubRegistryManager.from_connection_string(IOT_HUB_CONN_STR)
except Exception as e:
    logging.error(f"Error initializing Registry Manager: {e}")
    # Handle this in a real app, maybe raise an exception or set manager to None


def main(req: object) -> dict:
    """
    An Azure Function to invoke a direct method on an IoT Edge/Hub device.
    """
    logging.info('Device command function triggered.')
    
    try:
        # --- 1. Extract the method name and payload from the HTTP request body ---
        # The exact way you parse 'req' depends on your Function trigger type (e.g., HTTP, Timer)
        # For an HTTP trigger, you'd typically get the body like this:
        req_body = req.get_json()
        device_id = req_body.get('deviceId', DEVICE_ID)
        method_name = req_body.get('methodName', 'defaultMethod') 
        command_payload_dict = req_body.get('payload', {}) # The dict of arguments for the device
        
        # --- 2. 💡 THE FIX: Create the correct SDK object ---
        # The registry_manager.invoke_device_method function expects an object 
        # from the SDK, not a raw Python dictionary.
        
        method_payload = CloudToDeviceMethod(
            method_name=method_name,
            payload=command_payload_dict,
            # Set a reasonable timeout for the device to respond
            response_timeout_in_seconds=30 
        )

        # --- 3. Invoke the Device Method ---
        logging.info(f"Invoking method '{method_name}' on device '{device_id}'...")
        
        # 💡 This call now succeeds because method_payload is a CloudToDeviceMethod object
        response = registry_manager.invoke_device_method(device_id, method_payload)

        # --- 4. Process the response ---
        if response and response.status in [200, 201]:
            logging.info(f"Command successful. Status: {response.status}")
            return {
                "status": "Success",
                "methodResponse": response.payload
            }
        else:
            logging.error(f"Command failed. Status: {response.status}, Error: {response.payload}")
            return {
                "status": "Failure",
                "statusCode": response.status,
                "error": response.payload
            }

    except AttributeError as e:
        # This catch is for the original error if it happened somewhere else, 
        # but the fix above should prevent it in the invoke_device_method call.
        logging.error(f"An expected object attribute error occurred: {e}")
        return {"status": "Failure", "error": "Invalid payload format sent to SDK.", "details": str(e)}

    except Exception as e:
        logging.error(f"An unexpected error occurred while sending command: {e}")
        # The traceback shows this logging line:
        # 2025-09-28T15:50:41Z   [Error]   An unexpected error occurred while sending command
        return {"status": "Failure", "error": "Internal server error.", "details": str(e)}

# Note: You also need a 'function.json' file to define your function's trigger and bindings.
