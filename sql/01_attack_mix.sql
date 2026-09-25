-- What is the benign and attack-class distribution?
SELECT attack_label,COUNT(*) flows,ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (),2) share_pct FROM flow_enriched GROUP BY 1 ORDER BY flows DESC;
