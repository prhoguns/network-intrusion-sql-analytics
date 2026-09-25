-- Which labels feature SYN-heavy flows?
SELECT attack_label,COUNT(*) flows,ROUND(100.0*AVG((syn_flags>0)::INT),2) with_syn_pct,ROUND(AVG(syn_flags),3) mean_syn_flags FROM flow_enriched GROUP BY 1 ORDER BY flows DESC;
