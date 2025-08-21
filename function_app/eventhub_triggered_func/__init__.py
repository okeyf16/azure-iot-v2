import logging
import os
import json
import azure.functions as func
from azure.data.tables import TableServiceClient, UpdateMode
from azure.identity import DefaultAzureCredential
from datetime import datetime
import uuid

def main(event: func.EventHubEvent):
    logging.info('EventHub trigger function processed a message.')

    try:
        # Parse the Event Hub message as JSON
        message = event.get_body().decode('utf-8')
        data = json.loads(message)

        logging.info(f"Parsed message: {data}")

        # Environment variable with table name
        table_name = os.getenv("TABLE_NAME")

        if not table_name:
            logging.error("TABLE_NAME environment variable not set.")
            return

        # Connect using Managed Identity
        credential = DefaultAzureCredential()
        storage_account_url = os.getenv("STORAGE_ACCOUNT_URL")  # Inject via Terraform
        table_service = TableServiceClient(endpoint=storage_account_url, credential=credential)
        table_client = table_service.get_table_client(table_name)

        # Construct a row to insert
        row = {
            "PartitionKey": data.get("deviceId", "unknown"),
            "RowKey": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            **data
        }

        table_client.upsert_entity(entity=row, mode=UpdateMode.MERGE)
        logging.info(f"Row inserted to table: {row}")

    except Exception as e:
        logging.error(f"Error processing EventHub message: {str(e)}")
