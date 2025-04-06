{{ config(materialized='table') }}  

SELECT  
    event_id,  
    user_id,  
    amount,  
    currency,  
    status,
    ingested_at,  
    CASE  
        WHEN status = 'chargeback' THEN TRUE  
        ELSE FALSE  
    END AS is_chargeback,  
    CURRENT_TIMESTAMP AS dbt_updated_at  
FROM {{ source('public', 'raw_payments') }}  