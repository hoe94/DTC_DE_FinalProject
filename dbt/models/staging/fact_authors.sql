{{config(materialized = 'table')}}

select *
from {{ source('staging','goodreads_authors') }}