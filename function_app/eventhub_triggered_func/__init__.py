import logging
import os
import json
import uuid
import azure.functions as func
from datetime import datetime

# The 'outputTable' parameter is the output binding
def main(event: func.EventHubEvent, outputTable: func.Out[func.HttpResponse]):
    logging.info('EventHub trigger function processed a message.')
    logging.info(event.get_body().decode())

    try:
        # Parse the Event Hub message
        message = event.get_body().decode('utf-8')
        data = json.loads(message)

        logging.info(f"Parsed message: {data}")

        # Construct the entity for the output binding
        # The output binding automatically handles upserting the entity to the table
        output_entity = {
            "PartitionKey": data.get("deviceId", "unknown"),
            "RowKey": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            **data
        }

        # Set the output binding
        outputTable.set(json.dumps(output_entity))
        
        logging.info(f"✅ Entity sent to output binding: {output_entity}")

    except Exception as e:
        logging.error(f"❌ Error processing EventHub message: {str(e)}")


