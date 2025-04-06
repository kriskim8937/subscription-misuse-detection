{{ config(materialized='table') }}  

WITH login_metrics AS (  
    SELECT  
        user_id,  
        COUNT(DISTINCT ip_address) AS unique_ips_24h,  
        COUNT(DISTINCT device_id) AS unique_devices_24h  
    FROM {{ ref('stg_login_attempts') }}  
    WHERE ingested_at >= CURRENT_TIMESTAMP - INTERVAL '24 hours'  
    GROUP BY 1  
)  

SELECT  
    user_id,  
    unique_ips_24h,  
    unique_devices_24h,  
    CASE  
        WHEN unique_ips_24h > 3 OR unique_devices_24h > 2 THEN 'HIGH_RISK'  
        WHEN unique_ips_24h > 1 THEN 'MEDIUM_RISK'  
        ELSE 'LOW_RISK'  
    END AS misuse_risk_level,  
    CURRENT_TIMESTAMP AS detected_at  
FROM login_metrics  