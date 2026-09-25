-- How do top attacked ports change across days?
WITH top_ports AS (SELECT dst_port FROM flow_enriched GROUP BY 1 ORDER BY SUM(is_attack::INT) DESC LIMIT 8) SELECT source_day,dst_port,COUNT(*) flows,SUM(is_attack::INT) attacks FROM flow_enriched WHERE dst_port IN (SELECT dst_port FROM top_ports) GROUP BY 1,2 ORDER BY 1,4 DESC;
