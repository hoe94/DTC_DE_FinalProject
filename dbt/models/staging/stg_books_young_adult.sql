{{ config(materialized='view') }}

select *
from {{ source('staging','goodreads_books_young_adult') }}