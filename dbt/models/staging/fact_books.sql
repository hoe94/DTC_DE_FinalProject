{{ config(materialized='table') }}

with poetry as (
    select *, 'poetry' as book_type
    from {{ ref('stg_books_poetry') }} 
)

select * from poetry