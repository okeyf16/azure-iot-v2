import logging
import os
import json
import azure.functions as func
from azure.data.tables import TableServiceClient, UpdateMode
from datetime import datetime
import uuid

def main(event: func.EventHubEvent):
    logging.info('EventHub trigger function processed a message.')

    try:
        # Parse the Event Hub message
        message = event.get_body().decode('utf-8')
        data = json.loads(message)

        logging.info(f"Parsed message: {data}")

        # Environment variables
        table_name = os.getenv("TABLE_NAME")
        connection_string = os.getenv("TelemetryStorage")

        if not table_name or not connection_string:
            logging.error("TABLE_NAME or TelemetryStorage environment variable not set.")
            return

        # Connect using connection string
        table_service = TableServiceClient.from_connection_string(conn_str=connection_string)
        table_client = table_service.get_table_client(table_name)

        # Ensure table exists (idempotent)
        try:
            table_client.create_table()
        except Exception:
            pass  # table already exists

        # Construct row
        row = {
            "PartitionKey": data.get("deviceId", "unknown"),
            "RowKey": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            **data
        }

        table_client.upsert_entity(entity=row, mode=UpdateMode.MERGE)
        logging.info(f"✅ Row inserted to table: {row}")

    except Exception as e:
        logging.error(f"❌ Error processing EventHub message: {str(e)}")
