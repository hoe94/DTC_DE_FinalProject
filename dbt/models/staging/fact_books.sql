{{ config(materialized='table') }}

with children as (
    select *, 'children' as book_type
    from {{ ref('stg_books_children') }} 
),

comics_graphic as (
    select *, 'comics_graphic' as book_type
    from {{ ref('stg_books_comics_graphic') }} 
),

fantasy_paranormal as (
    select *, 'fantasy_paranormal' as book_type
    from {{ ref('stg_books_fantasy_paranormal') }} 
),

history_biography as (
    select *, 'history_biography' as book_type
    from {{ ref('stg_books_history_biography') }} 
),

mystery_thriller_crime as (
    select *, 'mystery_thriller_crime' as book_type
    from {{ ref('stg_books_mystery_thriller_crime') }} 
),

poetry as (
    select *, 'poetry' as book_type
    from {{ ref('stg_books_poetry') }} 
),

romance as (
    select *, 'poetry' as book_type
    from {{ ref('stg_books_romance') }} 
),

young_adult as (
    select *, 'poetry' as book_type
    from {{ ref('stg_books_young_adult') }} 
),

books as (
    select * from children
    union all
    select * from comics_graphic
    union all
    select * from fantasy_paranormal
    union all
    select * from history_biography
    union all
    select * from mystery_thriller_crime
    union all
    select * from poetry
    union all
    select * from romance
    union all
    select * from young_adult
)

select * from books