{{ config(materialized='view') }}

select *
from {{ source('staging','goodreads_books_history_biography') }}