# DTC_DE_FinalProject
This is the final project that after participated the Data Engineering Zoomcamp among 7 weeks. The course is organized by [DataTalks.Club](https://datatalks.club). It's my honor to learnt many technologies (docker, airflow, spark, kafka) related to DE FOC. Appreciated the instructors put so much effort on this course, they are spending the time to prepare the course but do reply the student's inquiry in the slack channel.

## Project Description
This is the end to end project to gain the insight about the books & books reviews from [GoodReads](https://www.goodreads.com/). And this project covers the scope of data engineering (build the data pipeline) & data analytic (build the data dashboard). There are 2 main module for this project, Books & Reviews.
We will build the data ingestion pipeline based on Apache Airflow. Besides, we are using DBT to perform the data transformation. At the end, we will use Google Data Studio to build the visualization dashboard.

## Objective
  * Books Module: User can gain the deeper insight of all the available books from GoodReads
  * Reviews Module: User can analyze the reader ratings and discover the current market trend

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
We have categorized all the airflow jobs by using TAGS as there are 2 modules for this project. 
For each module, there are 3 different kind of job to perform the data ingestion
 * goodreads_[module]_download_dag:
   * download the gz file from data source
   * extract out the json file from gz file
 
