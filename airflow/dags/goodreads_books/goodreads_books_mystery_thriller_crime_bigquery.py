import os

from google.cloud import bigquery
from google.cloud.bigquery import SourceFormat, LoadJobConfig
from google.cloud.bigquery.table import Table

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

BUCKET = os.environ.get("GCP_GCS_BUCKET")
client = bigquery.Client()
dataset_name = 'goodreads_book'
dataset_ref = client.dataset(dataset_name)


def bigquery_create_table(bucket):
    csv_file = 'goodreads_books_mystery_thriller_crime.csv'
    table_name = 'goodreads_books_mystery_thriller_crime'
    try:
        gcs_csv_uri = f"gs://{bucket}/raw/{csv_file}"
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
    dag_id = "goodreads_books_mystery_thriller_crime_bigquery",
    #schedule_interval="@monthly",
    default_args = default_args,
    catchup = True,
    max_active_runs = 1,
    tags = ['books'],
) as dag:

    gcs_bigquery = PythonOperator(
        task_id = "gcs_bigquery",
        python_callable = bigquery_create_table,
        op_kwargs = {
            "bucket": BUCKET ,
        }
    )