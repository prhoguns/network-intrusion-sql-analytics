-- How do labels distribute across network protocols?
SELECT protocol,attack_label,COUNT(*) flows FROM flow_enriched GROUP BY 1,2 ORDER BY 1,3 DESC;
