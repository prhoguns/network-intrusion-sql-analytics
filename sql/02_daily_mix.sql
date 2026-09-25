-- How does traffic composition change by source day?
SELECT source_day,attack_label,COUNT(*) flows FROM flow_enriched GROUP BY 1,2 ORDER BY 1,3 DESC;
