-- Which destination ports receive the most labeled attacks?
SELECT dst_port,COUNT(*) flows,SUM(is_attack::INT) attacks,ROUND(100.0*AVG(is_attack::INT),2) attack_pct FROM flow_enriched GROUP BY 1 ORDER BY attacks DESC LIMIT 20;
