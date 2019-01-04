from google.cloud import bigquery
from google.oauth2 import service_account
from google.api_core.exceptions import NotFound
import os

credentials = service_account.Credentials.from_service_account_file('gcp_data_upload.json')
project_id = 'tgd-meu-open-data'
client = bigquery.Client(credentials=credentials, project=project_id)


# Note - this requires a recent >=0.21 version of pandas, and a parquet library like pyarrow.  Can't get it to work.
def upload_data_frame_to_gcp(df, dataset_id, table_id, delete_existing=True):
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1
    job_config.autodetect = True

    # Note - this requires a recent >=0.21 version of pandas, and a parquet library like pyarrow.  Can't get it to work.
    # job = client.load_table_from_dataframe(
    #     df,
    #     table_ref,
    #     location='US',  # Must match the destination dataset location.
    #     job_config=job_config)  # API request

    if delete_existing:
        delete_table_from_gcp(dataset_id, table_id)

    csv_file_path = 'data/to_gcp_{}_{}.csv'.format(dataset_id, table_id)
    df.to_csv(csv_file_path, sep="|", encoding='utf-8', index=False)
    with open(csv_file_path, 'rb') as source_file:
        job = client.load_table_from_file(
            source_file,
            table_ref,
            location='US',  # Must match the destination dataset location.
            job_config=job_config)  # API request
    job.result()  # Waits for table load to complete.

    os.remove(csv_file_path)

    print('Loaded {} rows into {}:{}.'.format(job.output_rows, dataset_id, table_id))


def delete_table_from_gcp(dataset_id, table_id, verbose=False):
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    try:
        client.delete_table(table_ref)
    except NotFound as err:
        if verbose:
            print err


def table_exists(dataset_id, table_id):
    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    try:
        client.get_table(table_ref)
        return True
    except NotFound as err:
        return False


def execute_query(query_str):
    return client.query(query_str).result().to_dataframe()
