{{ config(materialized='table') }}  

SELECT  
    p.user_id,  
    COUNT(CASE WHEN p.status = 'failed' THEN 1 END) AS failed_payments_7d,  
    COUNT(CASE WHEN p.is_chargeback THEN 1 END) AS chargebacks_30d  
FROM {{ ref('stg_payment_events') }} p  
GROUP BY 1  