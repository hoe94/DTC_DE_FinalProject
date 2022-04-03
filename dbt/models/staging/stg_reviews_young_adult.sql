{{ config(materialized='view') }}

select *
from {{ source('staging','goodreads_reviews_young_adult') }}