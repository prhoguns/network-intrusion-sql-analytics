-- How does flow duration differ by label?
SELECT attack_label,COUNT(*) flows,ROUND(QUANTILE_CONT(duration_s,0.5),3) median_s,ROUND(QUANTILE_CONT(duration_s,0.95),3) p95_s FROM flow_enriched WHERE duration_s>=0 GROUP BY 1 ORDER BY flows DESC;
