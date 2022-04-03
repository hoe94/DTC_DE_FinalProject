import os
import logging
from datetime import datetime
import pandas as pd

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from google.cloud import storage

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
airflow_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")


json_file_list = airflow_home + '/goodreads_books_history_biography.json',
csv_file_list = airflow_home + '/goodreads_books_history_biography.csv',
csv_file = 'goodreads_books_history_biography.csv',

def convert_json_csv_books(json_file, csv_file):
    try:
        df = pd.read_json(json_file, lines=True)
        df.to_csv(csv_file, index = False)
        print('The conversion job is done!')
    except Exception as e:
        print(e)
    
def upload_to_gcs(bucket, local_file, gcs_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name
    :param object_name: target path & file-name
    :param local_file: source path & file-name
    :return:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    try:
        client = storage.Client()
        bucket = client.bucket(bucket)

        blob = bucket.blob(local_file)
        blob.upload_from_filename(gcs_file)
        print('The upload job is done!')
    except Exception as e:
        print(e)

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    #"start_date": datetime(2019,1,1),
    #"end_date":   datetime(2019,12,1),
    "depends_on_past": False,
    "retries": 1
}

with DAG(
    dag_id = "goodreads_books_history_biography_conversion",
    #schedule_interval="@monthly",
    default_args = default_args,
    catchup = True,
    max_active_runs = 1,
    tags = ['books'],
) as dag:

    convert_json_csv_history = PythonOperator(
        task_id = "convert_json_csv_history",
        python_callable = convert_json_csv_books,
        op_kwargs = {
            "json_file": airflow_home + '/goodreads_books_history_biography.json',
            "csv_file": airflow_home + '/goodreads_books_history_biography.csv',

        }
    )

    local_to_gcs_task = PythonOperator(
        task_id = "local_to_gcs_task",
        python_callable = upload_to_gcs,
        op_kwargs = {
            "bucket": BUCKET,
            "local_file": "raw/goodreads_books_history_biography.csv",
            "gcs_file": "goodreads_books_history_biography.csv",
        },
    )
    convert_json_csv_history >> local_to_gcs_task