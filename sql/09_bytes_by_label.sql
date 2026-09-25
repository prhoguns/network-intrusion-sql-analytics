-- How much data does a typical flow carry by label?
SELECT attack_label,COUNT(*) flows,ROUND(QUANTILE_CONT(total_bytes,0.5),1) median_bytes,ROUND(QUANTILE_CONT(total_bytes,0.95),1) p95_bytes FROM flow_enriched WHERE total_bytes>=0 GROUP BY 1 ORDER BY flows DESC;
