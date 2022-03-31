{{ config(materialized='view') }}

select *
from {{ source('staging','goodreads_books_comics_graphic') }}