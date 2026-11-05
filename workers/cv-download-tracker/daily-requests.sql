-- New, hardened counter only. One row per UTC day and CV language.
-- A request is neither a unique visitor nor a completed PDF download.
-- Empty days are absent: fill them with zero in the visualisation if needed.
SELECT
  toStartOfDay(timestamp) AS day_utc,
  blob1 AS cv_language,
  SUM(_sample_interval * double1) AS cv_requests
FROM guillaume_sabiron_cv_downloads
WHERE timestamp >= NOW() - INTERVAL '30' DAY
  AND blob2 = 'cv_request'
GROUP BY day_utc, cv_language
ORDER BY day_utc, cv_language
