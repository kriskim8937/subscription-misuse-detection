{{ config(materialized='table') }}  

SELECT  
    user_id,  
    plan_id,  
    timestamp,
    is_trial
FROM {{ source('public', 'raw_subscriptions') }}  