{{ config(materialized='table') }}  

WITH trial_users AS (  
    SELECT  
        user_id,  
        COUNT(*) AS trial_count  
    FROM {{ ref('stg_user_subscriptions') }}  
    WHERE is_trial = TRUE  
    GROUP BY 1  
)  

SELECT  
    user_id,  
    trial_count,  
    CASE  
        WHEN trial_count > 1 THEN TRUE  
        ELSE FALSE  
    END AS is_trial_abuser  
FROM trial_users  