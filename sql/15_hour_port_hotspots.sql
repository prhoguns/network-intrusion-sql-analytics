-- Which hour-port combinations concentrate attack volume?
SELECT hour_start,dst_port,COUNT(*) flows,SUM(is_attack::INT) attacks,ROUND(100.0*AVG(is_attack::INT),2) attack_pct FROM flow_enriched GROUP BY 1,2 HAVING COUNT(*)>=100 ORDER BY attacks DESC LIMIT 30;
