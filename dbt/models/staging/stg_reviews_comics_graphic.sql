{{ config(materialized='view') }}

select *
from {{ source('staging','goodreads_reviews_comics_graphic') }}