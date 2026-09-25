-- What share of flows are short and packet-light?
SELECT attack_label,COUNT(*) flows,ROUND(100.0*AVG((duration_s<1 AND fwd_pkts<=3)::INT),2) short_small_pct FROM flow_enriched WHERE duration_s>=0 GROUP BY 1 ORDER BY flows DESC;
