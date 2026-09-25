-- How does packet rate vary by label?
SELECT attack_label,COUNT(*) flows,ROUND(QUANTILE_CONT(pkts_per_s,0.5),2) median_pkts_s,ROUND(QUANTILE_CONT(pkts_per_s,0.95),2) p95_pkts_s FROM flow_enriched WHERE isfinite(pkts_per_s) AND pkts_per_s>=0 GROUP BY 1 ORDER BY flows DESC;
