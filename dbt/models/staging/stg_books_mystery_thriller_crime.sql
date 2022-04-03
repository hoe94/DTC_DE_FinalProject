{{ config(materialized='view') }}

select *
from {{ source('staging','goodreads_books_mystery_thriller_crime') }}