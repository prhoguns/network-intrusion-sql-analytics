-- How does labeled attack rate vary by hour?
SELECT hour_start,COUNT(*) flows,SUM(is_attack::INT) attacks,ROUND(100.0*AVG(is_attack::INT),2) attack_pct FROM flow_enriched GROUP BY 1 ORDER BY 1;
