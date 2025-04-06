{{ config(materialized='table') }}  

SELECT  
    u.user_id,  
    u.plan_id,
    l.misuse_risk_level AS login_risk,  
    p.chargebacks_30d > 0 AS has_chargeback,  
    t.is_trial_abuser,
    l.detected_at
FROM {{ ref('stg_user_subscriptions') }} u  
LEFT JOIN {{ ref('int_suspicious_logins') }} l ON u.user_id = l.user_id  
LEFT JOIN {{ ref('int_failed_payments') }} p ON u.user_id = p.user_id  
LEFT JOIN {{ ref('int_trial_abusers') }} t ON u.user_id = t.user_id  