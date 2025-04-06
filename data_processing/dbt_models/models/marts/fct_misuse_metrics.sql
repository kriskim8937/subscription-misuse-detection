{{ config(materialized='table') }}  

SELECT  
    DATE_TRUNC('day', detected_at) AS date,  
    COUNT(DISTINCT CASE WHEN login_risk = 'HIGH_RISK' THEN user_id END) AS high_risk_users,  
    COUNT(DISTINCT CASE WHEN has_chargeback THEN user_id END) AS chargeback_users,  
    COUNT(DISTINCT CASE WHEN is_trial_abuser THEN user_id END) AS trial_abusers  
FROM {{ ref('dim_misuse_cases') }}  
GROUP BY 1  