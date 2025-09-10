import logging
import os
import json
import azure.functions as func
from datetime import datetime
import uuid

# Note: TableServiceClient and UpdateMode are no longer needed because the output binding handles the connection.

def main(event: func.EventHubEvent, outputTable: func.Out[str]):
    logging.info('EventHub trigger function processed a message.')
    logging.info(event.get_body().decode())

    try:
        # Parse the Event Hub message
        message = event.get_body().decode('utf-8')
        data = json.loads(message)

        logging.info(f"Parsed message: {data}")

        # Construct row
        row = {
            "PartitionKey": data.get("deviceId", "unknown"),
            "RowKey": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            **data
        }

        # Use the output binding to write the data to the table
        # This is where the magic happens; the host manages the connection.
        outputTable.set(json.dumps(row))
        logging.info(f"✅ Row inserted to table: {row}")

    except Exception as e:
        logging.error(f"❌ Error processing EventHub message: {str(e)}")
