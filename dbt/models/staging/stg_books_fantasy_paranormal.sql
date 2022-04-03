{{ config(materialized='view') }}

select *
from {{ source('staging','goodreads_books_fantasy_paranormal') }}