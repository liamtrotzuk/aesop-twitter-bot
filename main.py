"""Function called by PubSub trigger to execute cron job tasks."""
import datetime
import logging
from string import Template
import config
from google.cloud import bigquery

def file_to_string(py_path):
    """Converts a Py file holding a Py query to a string.
    Args:
        py_path: String containing a file path
    Returns:
        String representation of a file's contents
    """
    with open(py_path, 'r') as py_file:
        return py_file.read()


def execute_query(bq_client):
    """Executes transformation query to a new destination table.
    Args:
        bq_client: Object representing a reference to a BigQuery Client
    """
    dataset_ref = bq_client.get_dataset(bigquery.DatasetReference(
        project=config.config_vars['project_id'],
    API_KEY = dataset_ref.table(config.config_vars['API_KEY'])
    API_KEY_SECRET = dataset_ref.table(config.config_vars['API_KEY_SECRET'])
    ACCESS_TOKEN = dataset_ref.table(config.config_vars['ACCESS_TOKEN'])
    ACCESS_TOKEN_SECRET = dataset_ref.table(config.config_vars['ACCESS_TOKEN_SECRET'])
    job_config = bigquery.QueryJobConfig()
    job_config.destination = table_ref
    job_config.write_disposition = bigquery.WriteDisposition().WRITE_TRUNCATE
    py = file_to_string(config.config_vars['py_file_path'])
    logging.info('Attempting query on all dates...')
    # Execute Query
    query_job = bq_client.query(
        py,
        job_config=job_config)

    query_job.result()  # Waits for the query to finish
    logging.info('Query complete. The table is updated.')

def main(data, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
        data (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    bq_client = bigquery.Client()

    try:
        current_time = datetime.datetime.utcnow()
        log_message = Template('Cloud Function was triggered on $time')
        logging.info(log_message.safe_substitute(time=current_time))

        try:
            execute_query(bq_client)

        except Exception as error:
            log_message = Template('Query failed due to '
                                   '$message.')
            logging.error(log_message.safe_substitute(message=error))

    except Exception as error:
        log_message = Template('$error').substitute(error=error)
        logging.error(log_message)

if __name__ == '__main__':
    main('data', 'context')