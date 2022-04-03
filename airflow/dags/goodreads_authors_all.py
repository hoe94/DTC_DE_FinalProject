import os
import logging
from datetime import datetime
import gdown
import gzip, shutil
import pandas as pd

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from google.cloud import storage, bigquery
from google.cloud.bigquery import SourceFormat, LoadJobConfig
from google.cloud.bigquery.table import Table

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
airflow_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
storage_client = storage.Client()
client = bigquery.Client()
dataset_name = 'goodreads_book'
dataset_ref = client.dataset(dataset_name)

gdrive_book_list = ['https://drive.google.com/uc?id=19cdwyXwfXx_HDIgxXaHzH0mrx8nMyLvC']
gz_file_list = [airflow_home + '/goodreads_authors.gz']
json_file_list = [airflow_home + '/goodreads_authors.json']
csv_file_list = [airflow_home + '/goodreads_authors.csv']
csv_file = ['goodreads_authors.csv']
table_list = ['goodreads_authors']

def download_task():
    gdrive_gz_file = zip(gdrive_book_list, gz_file_list)
    for i in gdrive_gz_file:
        gdrive_file_location = i[0]
        gz_file_location = i[1]
        gdown.download(gdrive_file_location, output = gz_file_location, quiet = False)

def unzip_gz_file():
    gz_json_file = zip(gz_file_list, json_file_list)
    for i in gz_json_file:
        gz_file_location = i[0]
        json_file_location = i[1]
        with gzip.open(gz_file_location, 'rb') as f_in,  open(json_file_location, 'wb') as f_out:
             shutil.copyfileobj(f_in, f_out)

def convert_json_csv_upload_gcs(bucket_param, object_name, local_file):
    json_csv_file = zip(json_file_list, csv_file_list)
    for i in json_csv_file:
        json_file_location = i[0]
        csv_file_location = i[1]
        df = pd.read_json(json_file_location, lines=True)
        df.to_csv(csv_file_location, index = False)

        storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
        storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB

        bucket = storage_client.bucket(bucket_param)
        blob = bucket.blob(object_name)
        blob.upload_from_filename(local_file)

def bigquery_create_table(bucket):
    gbq_list = zip(csv_file, table_list)
    for i in gbq_list:
        csv_file_ = i[0]
        table_name = i[1]
        try:
            gcs_csv_uri = f"gs://{bucket}/raw/{csv_file_}"
            full_table_id = f"dtc-de-course-hoe.goodreads_book.{table_name}"
            job_config = LoadJobConfig(
                autodetect = True,
                skip_leading_rows = 1,
                source_format = SourceFormat.CSV,
                destination_table_friendly_name = table_name
            )
            job_config.allow_quoted_newlines = True
            load_job = client.load_table_from_uri(
                gcs_csv_uri, full_table_id, job_config = job_config
            )
            print(f"Starting job {load_job.job_id}.")
            print(load_job.result())  # Waits for table load to complete.
        except Exception as e:
            print(f"Unexpected error when creating table `{full_table_id}`: {e}")

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    #"start_date": datetime(2019,1,1),
    #"end_date":   datetime(2019,12,1),
    "depends_on_past": False,
    "retries": 1
}

with DAG(
    dag_id = "goodreads_authors_all_dag",
    #schedule_interval="@monthly",
    default_args = default_args,
    catchup = True,
    max_active_runs = 1,
    tags = ['authors'],
) as dag:

    download_task = PythonOperator(
        task_id = "download_task",
        python_callable = download_task
    )

    unzip_gz_file = PythonOperator(
        task_id = "unzip_gz_file",
        python_callable = unzip_gz_file
    )

    convert_json_csv_upload_gcs = PythonOperator(
        task_id = "convert_json_csv_upload_gcs",
        python_callable = convert_json_csv_upload_gcs,
        op_kwargs = {
            "bucket_param": BUCKET ,
            "object_name": "raw/goodreads_authors.csv",
            "local_file": "goodreads_authors.csv"
        }
    )

    gcs_bigquery = PythonOperator(
        task_id = "gcs_bigquery",
        python_callable = bigquery_create_table,
        op_kwargs = {
            "bucket": BUCKET ,
        }
    )

    #download_task >> unzip_gz_file >> convert_json_csv >> local_to_gcs_task
    #download_task >> unzip_gz_file
    download_task >> unzip_gz_file >> convert_json_csv_upload_gcs >> gcs_bigquery