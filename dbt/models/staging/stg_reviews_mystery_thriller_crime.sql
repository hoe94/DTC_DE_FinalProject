{{ config(materialized='view') }}

select *
from {{ source('staging','goodreads_reviews_mystery_thriller_crime') }}