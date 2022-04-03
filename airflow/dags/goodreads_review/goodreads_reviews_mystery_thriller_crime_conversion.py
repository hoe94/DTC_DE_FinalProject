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


json_file_list = airflow_home + '/goodreads_reviews_mystery_thriller_crime.json',
csv_file_list = airflow_home + '/goodreads_reviews_mystery_thriller_crime.csv',
csv_file = 'goodreads_reviews_mystery_thriller_crime.csv',

def convert_json_csv_books(json_file, csv_file, bucket, object_name, local_file):
    df = pd.read_json(json_file, lines=True)
    df.to_csv(csv_file, index = False)
    
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    
    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)
    
#def upload_to_gcs(bucket):
#    """
#    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
#    :param bucket: GCS bucket name
#    :param object_name: target path & file-name
#    :param local_file: source path & file-name
#    :return:
#    """
#    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
#    # (Ref: https://github.com/googleapis/python-storage/issues/74)
#    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
#    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
#    # End of Workaround
#    csv_file_dict = zip(csv_file_list, csv_file)
#
#    for i in csv_file_dict:
#        local_file = i[0]
#        gcs_file = i[1]
#
#        client = storage.Client()
#        bucket = client.bucket(bucket)
#
#        blob = bucket.blob(local_file)
#        blob.upload_from_filename(gcs_file)

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    #"start_date": datetime(2019,1,1),
    #"end_date":   datetime(2019,12,1),
    "depends_on_past": False,
    "retries": 1
}

with DAG(
    dag_id = "goodreads_reviews_mystery_thriller_crime_conversion",
    #schedule_interval="@monthly",
    default_args = default_args,
    catchup = True,
    max_active_runs = 1,
    tags = ['reviews'],
) as dag:

    convert_json_csv_mystery_thriller_crime = PythonOperator(
        task_id = "convert_json_csv_mystery_thriller_crime",
        python_callable = convert_json_csv_books,
        op_kwargs = {
            "json_file": airflow_home + '/goodreads_reviews_mystery_thriller_crime.json',
            "csv_file": airflow_home + '/goodreads_reviews_mystery_thriller_crime.csv',
            "bucket": BUCKET,
            "object_name": "raw/goodreads_reviews_mystery_thriller_crime.csv",
            "local_file": "goodreads_reviews_mystery_thriller_crime.csv"
        }
    )

    convert_json_csv_mystery_thriller_crime