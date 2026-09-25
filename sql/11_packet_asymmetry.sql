-- Which labels have forward-heavy packet patterns?
SELECT attack_label,COUNT(*) flows,ROUND(AVG(fwd_pkts),2) mean_fwd_pkts,ROUND(AVG(bwd_pkts),2) mean_bwd_pkts,ROUND(100.0*AVG((fwd_pkts>3*bwd_pkts+3)::INT),2) forward_heavy_pct FROM flow_enriched GROUP BY 1 ORDER BY flows DESC;
