-- Which labels have unusually upload-heavy flows?
SELECT attack_label,COUNT(*) flows,ROUND(100.0*AVG((upload_download_ratio>10)::INT),2) upload_heavy_pct,ROUND(QUANTILE_CONT(upload_download_ratio,0.5),2) median_ratio FROM flow_enriched WHERE fwd_bytes>=0 AND bwd_bytes>=0 GROUP BY 1 ORDER BY flows DESC;
