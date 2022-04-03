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

from google.cloud import storage

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")
airflow_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

gdrive_book_list = [
'https://drive.google.com/uc?id=1908GDMdrhDN7sTaI_FelSHxbwcNM1EzR',
'https://drive.google.com/uc?id=1V4MLeoEiPQdocCbUHjR_7L9ZmxTufPFe',
'https://drive.google.com/uc?id=1THnnmE4XSCvMkGOsqapQr2cJI5amKA6X',
'https://drive.google.com/uc?id=1lDkTzM6zpYU-HGkVAQgsw0dBzik-Zde9',
'https://drive.google.com/uc?id=1ONpyuv0vrtd6iUEp0-zzkKqwpm3njEqi',
'https://drive.google.com/uc?id=1FVD3LxJXRc5GrKm97LehLgVGbRfF9TyO',
'https://drive.google.com/uc?id=1NpFsDQKBj_lrTzSASfyKbmkSykzN88wE',
'https://drive.google.com/uc?id=1M5iqCZ8a7rZRtsmY5KQ5rYnP9S0bQJVo'
]

gz_file_list = [
    airflow_home + '/goodreads_reviews_children_json.gz',
    airflow_home + '/goodreads_reviews_comics_graphic_json.gz',
    airflow_home + '/goodreads_reviews_fantasy_paranormal_json.gz',
    airflow_home + '/goodreads_reviews_history_biography_json.gz',
    airflow_home + '/goodreads_reviews_mystery_thriller_crime_json.gz',
    airflow_home + '/goodreads_reviews_poetry_json.gz',
    airflow_home + '/goodreads_reviews_romance_json.gz',
    airflow_home + '/goodreads_reviews_young_adult_json.gz'
]

json_file_list = [
    airflow_home + '/goodreads_reviews_children.json',
    airflow_home + '/goodreads_reviews_comics_graphic.json',
    airflow_home + '/goodreads_reviews_fantasy_paranormal.json',
    airflow_home + '/goodreads_reviews_history_biography.json',
    airflow_home + '/goodreads_reviews_mystery_thriller_crime.json',
    airflow_home + '/goodreads_reviews_poetry.json',
    airflow_home + '/goodreads_reviews_romance.json',
    airflow_home + '/goodreads_reviews_young_adult.json'
]

csv_file_list = [
    airflow_home + '/goodreads_reviews_children.csv',
    airflow_home + '/goodreads_reviews_comics_graphic.csv',
    airflow_home + '/goodreads_reviews_fantasy_paranormal.csv',
    airflow_home + '/goodreads_reviews_history_biography.csv',
    airflow_home + '/goodreads_reviews_mystery_thriller_crime.csv',
    airflow_home + '/goodreads_reviews_poetry.csv',
    airflow_home + '/goodreads_reviews_romance.csv',
    airflow_home + '/goodreads_reviews_young_adult.csv'
]

csv_file = [
    'goodreads_reviews_children.csv',
    'goodreads_reviews_comics_graphic.csv',
    'goodreads_reviews_fantasy_paranormal.csv',
    'goodreads_reviews_history_biography.csv',
    'goodreads_reviews_mystery_thriller_crime.csv',
    'goodreads_reviews_poetry.csv',
    'goodreads_reviews_romance.csv',
    'goodreads_reviews_young_adult.csv'
]

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

#def convert_json_csv():
#    json_csv_file = zip(json_file_list, csv_file_list)
#    for i in json_csv_file:
#        json_file_location = i[0]
#        csv_file_location = i[1]
#        df = pd.read_json(json_file_location, lines=True)
#        df.to_csv(csv_file_location, index = False)

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
    dag_id = "goodreads_reviews_download_dag",
    #schedule_interval="@monthly",
    default_args = default_args,
    catchup = True,
    max_active_runs = 1,
    tags = ['reviews'],
) as dag:

    download_task = PythonOperator(
        task_id = "download_task",
        python_callable = download_task
    )

    unzip_gz_file = PythonOperator(
        task_id = "unzip_gz_file",
        python_callable = unzip_gz_file
    )

    #convert_json_csv = PythonOperator(
    #    task_id = "convert_json_csv",
    #    python_callable = convert_json_csv
    #)

    #local_to_gcs_task = PythonOperator(
    #    task_id = "local_to_gcs_task",
    #    python_callable = upload_to_gcs,
    #    op_kwargs = {
    #        "bucket": BUCKET
    #    },
    #)

    #download_task >> unzip_gz_file >> convert_json_csv >> local_to_gcs_task
    download_task >> unzip_gz_file