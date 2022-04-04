# DTC_DE_FinalProject
This is the final project that after participated the Data Engineering Zoomcamp among 7 weeks. This course is organized by [DataTalks.Club](https://datatalks.club). It's my honor to learnt many technologies (docker, airflow, spark, kafka) related to DE FOC. Appreciated the instructors put so much effort on this course, they are spending the time to prepare the course in video & github but do reply the student's inquiry in the slack channel.

## Project Description
This is the end to end project to gain the insight about the books & books reviews from [GoodReads](https://www.goodreads.com/). And this project covers the scope of data engineering (build the data pipeline) & data analytic (build the data dashboard). There are 2 main module for this project, Books & Reviews.
We will build the data ingestion pipeline based on Apache Airflow. Besides, we are using DBT to perform the data transformation. At the end, we will use Google Data Studio to build the visualization dashboard.

## Objective
  * Books Module: User can gain the deeper insight of all the available books from GoodReads
  * Reviews Module: User can analyze the reader reviews and discover the current market trend

## Dataset
MengTing Wan and her partners scrap the data in users' public shelves from [GoodReads](https://www.goodreads.com/) for the academic purpose. This dataset describes the books metadata & the reader reviwews. From the books metadata, we can understand the books further such as genre, language, published_year and etc. 
For the reader reviews, reader will provide the reviews/feedbacks for the books they have read.
And it consists of 8 different books genre for books & ratings module.
| Genre     					      |
|---|
|Children						        |
|Comics & Graphic				    |
|Fantasy & Paranormal			  |
|History & Biography			  |
|Mystery, Thriller & Crime	|
|Poetry							        |
|Romance						        |	
|Young Adult					       |

For whom are interested, You may find the data source at this [site](https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/home?authuser=0) 

## Tools & Technology
* Cloud: Google Cloud Platform (GCP)
  * Data Lake: Google Cloud Storage (GCS)
  * Data Warehouse: Google Big Query (GBQ)
  * Data Visualization: Google Data Studio (GDS)
* Containerization: Docker, Docker Compose
* Orchestration: Apache Airflow
* Data Transformation: Data Build Tool (DBT)
* Programming Language: Python, SQL

## Project Architecture
<img src = 'https://github.com/hoe94/DTC_DE_FinalProject/blob/main/images/Project_Architecture.png'>

## Data Ingestion Pipeline
We have categorized all the airflow jobs by using TAGS as there are 2 modules for this project. <br>
For each module, there are 3 different kind of job to perform the data ingestion. <br>
 * goodreads_[module]_download_dag:
   * download_task: download the gz file from data source
   * unzip_gz_file: extract out the json file from gz file
 * goodread_[module]_[books_genre]_conversion:
   * convert_json_csv_[module]: 
       * convert the json file into csv file
       * upload the csv file into data lake, google cloud storage (GCS)
 * goodreads_[module]_[books_genre]_bigquery:
   * gcs_bigquery: create the table in data warehouse, google big query (GBQ) by the csv file in GCS
<img alt = "image" src = "https://github.com/hoe94/DTC_DE_FinalProject/blob/main/images/1.png">

All the data will ingested into staging env (goodreads_books) as per below screenshot. <br>
Here is the Airflow DAG code for this project [link](https://github.com/hoe94/DTC_DE_FinalProject/tree/main/airflow) <br>
<img width = "437" alt = "image" src = "https://github.com/hoe94/DTC_DE_FinalProject/blob/main/images/3.png"> 

## Data Transformation Pipeline:
Due to the limited available time, We only perform 2 types data transformation for this project. <br>

1. Stack all the genres tables into the master table for books & reviews module.
<img width = "437" alt = "image" src = "https://github.com/hoe94/DTC_DE_FinalProject/blob/main/images/4.png"> <br>

2. Extract the date info from the string column in reviews module.<br>
<img width = "437" alt = "image" src = "https://github.com/hoe94/DTC_DE_FinalProject/blob/main/images/5.png"> 

All the processed data will ingested into production env (goodreads_stagging）.<br>
<img width = "437" alt = "image" src = "https://github.com/hoe94/DTC_DE_FinalProject/blob/main/images/6.png"> 

## Data Visualization
There are 2 dashboards for this project, GoodReads Books Dashboard & GoodReads Reviews Dashboard. <br>

Books Dashboard: [url](https://datastudio.google.com/u/1/reporting/a8e5ec4f-1cfa-4c94-8299-5fd6d4b9aa9e/page/kdepC)
Reviews Dashbaord: [url}(https://datastudio.google.com/u/1/reporting/a8e5ec4f-1cfa-4c94-8299-5fd6d4b9aa9e/page/p_mh4etteotc)

<img alt = "image" src = "https://github.com/hoe94/DTC_DE_FinalProject/blob/main/images/8.png">
<img alt = "image" src = "https://github.com/hoe94/DTC_DE_FinalProject/blob/main/images/9.png">

## Reproductivity

Step 0: Setup the Base Environment <br>
Required Services: <br>
* [Google Cloud Platform](https://console.cloud.google.com/) - register an account with credit card GCP will free us $300 (rm1200) for 3 months
  * Create a service account & download the keys as json file in IAM. The json file will be useful for further steps.
  * Enable the API related to the services (Google Compute Engine, Google Cloud Storage & Google Big Query)
* [Data Build Tools (DBT Cloud)](https://www.getdbt.com/signup/)
  * It's free usage for single user. Will start to configure at the below step

Step 1: Initial the Virtual Machine in Google Compute Engine
* create a linux based VM in GCS. Here is the tutorial video about setup the VM [video](https://www.youtube.com/watch?v=ae-CV2KfoN0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=12). The video start from beginning till 15 mins is the part about configure the VM in GCS.

Step 1.1: Create the bucket in Google Cloud Storage (GCS)
* create a folder, raw inside the GCS 

Step 1.2: Create the dataset in Google Big Query (GBQ)
* create a dataset, goodreads_books inside the GBQ

Step 1.3: Setup the Anaconda, Docker & Docker Compose in the Virtual Machine
* Install the *Remote SSH* extension in Visual Studio Code. This is useful while access the VM through SSH.
* Using the config file [here](https://github.com/hoe94/DTC_DE_FinalProject/tree/main/configuration) to access the VM through SSH.
* Here is the tutorial video about all the configuration [video](https://www.youtube.com/watch?v=ae-CV2KfoN0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=12)
  * The video start from 15 mins till 27 mins is the part about configuration
  * Setup the Anaconda, Docker & Docker Compose

Step 2: Setup the Apache Airflow through Docker Compose
* Create empty folder, airflow to contains the configuration file in VM
* Create empty folder, dags, logs, plugins inside the airflow folder
* Copy the dockerfile & docker-compose.yaml from the [repository](https://github.com/hoe94/DTC_DE_FinalProject/tree/main/configuration) & paste into airflow folder
* Change env variables GOOGLE_APPLICATION_CREDENTIALS (path to credentials file on VM), GCP_PROJECT_ID & GCP_GCS_BUCKET in docker-compose.yaml file
* Please refer this [tutorial video](https://www.youtube.com/watch?v=lqDMzReAtrw&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=18) for further details
* Run the docker command *docker-compose build* & *docker-compose up* to build the Airflow container through docker compose.
* Access the Airflow UI through this (url)[localhost:8080] and the credentials are username: airflow, password: airflow

Step 2.1: Data Ingestion Pipeline
* Copy all the dags file from [here](https://github.com/hoe94/DTC_DE_FinalProject/tree/main/airflow/dags) into dags folder in VM
* Run all the airflow jobs by enable the pipeline in Airflow UI.

Setup 3: DBT Cloud Configuration
* Please refer this [tutorial](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/week_4_analytics_engineering/dbt_cloud_setup.md) to setup the DBT Cloud. It requires the json file from step 0.

Setup 3.1: Data Transformation Pipeline
* Copy all the models file from [here](https://github.com/hoe94/DTC_DE_FinalProject/tree/main/dbt/models/staging) into this folder, models in DBT.
* Run the DBT command *dbt run --select fact_books* & *dbt run --select fact_reviews* to perform the data transformation. The processed data will ingested into Production env, goodreads_stagging

## Further Improvements:
* Add Streaming Pipeline (Apache Kafka) in this project
* Use Terraform to configure the services in Google Cloud
* Write .parquet file instead of .csv file in the data ingestion pipeline
* Schedule run the DBT models
* Write the data quality test in DBT
* Write the documentation in DBT
* Create the partitioned & clustered table in GBQ
* Perform more advanced data transformation by using DBT & Spark

## Special Thanks:
Kudos for [DataTalks.Club](https://datatalks.club) put so much effort on this courses to contribute the community. Without their contribution, we may learn the knowlegde from scratch & without the right guildance. You may visit here for the [course](https://github.com/DataTalksClub/data-engineering-zoomcamp) <br>

Besides, Thanks for MengTing Wan and her partners to provide the GoodReads Dataset. They are very kind to share their works to the public for the academic purpose.
I am glad to use the data source to start my final project. For whom are interested, You may find the data source at this [site](https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/home?authuser=0) <br>

Citation:
* Mengting Wan, Julian McAuley, ["Item Recommendation on Monotonic Behavior Chains"](https://www.google.com/url?q=https%3A%2F%2Fgithub.com%2FMengtingWan%2Fmengtingwan.github.io%2Fraw%2Fmaster%2Fpaper%2Frecsys18_mwan.pdf&sa=D&sntz=1&usg=AOvVaw0HcX6gU1ENhk7fbCXXbCiy)
in RecSys'18. [bibtext](https://www.google.com/url?q=https%3A%2F%2Fdblp.uni-trier.de%2Frec%2Fbibtex%2Fconf%2Frecsys%2FWanM18&sa=D&sntz=1&usg=AOvVaw2VTBdVH0HOCFqZJ3u3NsgZ)
* Mengting Wan, Rishabh Misra, Ndapa Nakashole, Julian McAuley, ["Fine-Grained Spoiler Detection from Large-Scale Review Corpora"](https://www.google.com/url?q=https%3A%2F%2Fwww.aclweb.org%2Fanthology%2FP19-1248&sa=D&sntz=1&usg=AOvVaw1G1ZlQ7oe0NDtqeI8gN2Nf), 
in ACL'19. [bibtex](https://www.google.com/url?q=https%3A%2F%2Fdblp.uni-trier.de%2Frec%2Fbibtex%2Fconf%2Facl%2FWanMNM19&sa=D&sntz=1&usg=AOvVaw25f7_0XLwNzo6a9-Qa2jGv)
