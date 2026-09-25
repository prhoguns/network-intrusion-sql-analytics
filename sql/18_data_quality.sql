-- How many curated flow values are missing or nonfinite?
SELECT source_day,COUNT(*) flows,COUNT(*) FILTER (WHERE dst_port IS NULL) missing_port,COUNT(*) FILTER (WHERE duration_s IS NULL) missing_duration,COUNT(*) FILTER (WHERE NOT isfinite(bytes_per_s)) nonfinite_bytes_per_s FROM flow_enriched GROUP BY 1 ORDER BY 1;
