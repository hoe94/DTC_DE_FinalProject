{{ config(materialized='table') }}

with children as (
    select *, 'children' as book_type
    from {{ ref('stg_reviews_children') }} 
),

comics_graphic as (
    select *, 'comics_graphic' as book_type
    from {{ ref('stg_reviews_comics_graphic') }} 
),

fantasy_paranormal as (
    select *, 'fantasy_paranormal' as book_type
    from {{ ref('stg_reviews_fantasy_paranormal') }} 
),

history_biography as (
    select *, 'history_biography' as book_type
    from {{ ref('stg_reviews_history_biography') }} 
),

mystery_thriller_crime as (
    select *, 'mystery_thriller_crime' as book_type
    from {{ ref('stg_reviews_mystery_thriller_crime') }} 
),

poetry as (
    select *, 'poetry' as book_type
    from {{ ref('stg_reviews_poetry') }} 
),

romance as (
    select *, 'poetry' as book_type
    from {{ ref('stg_reviews_romance') }} 
),

young_adult as (
    select *, 'poetry' as book_type
    from {{ ref('stg_reviews_young_adult') }} 
),

reviews as (
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

select *, 
CONCAT(substring(`date_updated`, -4), (case 
    when substring(`date_updated`, 5,3) = 'Jan' then '01'
    when substring(`date_updated`, 5,3) = 'Feb' then '02'
    when substring(`date_updated`, 5,3) = 'Mar' then '03'
    when substring(`date_updated`, 5,3) = 'Apr' then '04'
    when substring(`date_updated`, 5,3) = 'May' then '05'
    when substring(`date_updated`, 5,3) = 'Jun' then '06'
    when substring(`date_updated`, 5,3) = 'Jul'then '07'
    when substring(`date_updated`, 5,3) = 'Aug' then '08'
    when substring(`date_updated`, 5,3) = 'Sep' then '09'
    when substring(`date_updated`, 5,3) = 'Oct' then '10'
    when substring(`date_updated`, 5,3) = 'Nov' then '11'
    when substring(`date_updated`, 5,3) = 'Dec' then '12'
    ELSE '0'
END),substring(`date_updated`, 9,2)) AS data_updated_new
from reviews