{{ config(materialized='view') }}

SELECT
  user_id,
  device_id,
  ip_location,
  timestamp,
  DATE(timestamp) as activity_date,
  EXTRACT(HOUR FROM timestamp) as hour_of_day
FROM {{ source('public', 'raw_user_activity') }}
