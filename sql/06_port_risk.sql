-- Which common destination ports have the highest attack share?
SELECT dst_port,COUNT(*) flows,SUM(is_attack::INT) attacks,ROUND(100.0*AVG(is_attack::INT),2) attack_pct FROM flow_enriched GROUP BY 1 HAVING COUNT(*)>=1000 ORDER BY attack_pct DESC LIMIT 20;
