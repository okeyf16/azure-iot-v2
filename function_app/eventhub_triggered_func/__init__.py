import logging
import os
import json
import azure.functions as func
from datetime import datetime
import uuid

def main(event: func.EventHubEvent, outputTable: func.Out[str]):
    logging.info('EventHub trigger function processed a message.')
    
    try:
        # Parse the Event Hub message
        message = event.get_body().decode('utf-8')
        data = json.loads(message)

        logging.info(f"Parsed message: {data}")

        # Construct the entity for the output binding
        output_entity = {
            "PartitionKey": data.get("deviceId", "unknown"),
            "RowKey": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            **data
        }

        # Set the output binding. This writes the entity to the table.
        outputTable.set(json.dumps(output_entity))
        
        logging.info(f"✅ Entity sent to output binding: {output_entity}")

    except Exception as e:
        logging.error(f"❌ Error processing EventHub message: {str(e)}")
