{{ config(materialized='table') }}  

SELECT  
    user_id,  
    ip_address,  
    ingested_at,  
    device_id,  
    is_successful,  
    -- Add metadata for SOX compliance  
    CURRENT_TIMESTAMP AS dbt_updated_at  
FROM {{ source('public', 'raw_login_attempts') }}  