from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
raw = ROOT/'data/raw'
files = [raw/f'{day}.csv' for day in
 ('Wednesday-14-02-2018','Thursday-01-03-2018','Friday-02-03-2018')]
if not all(p.exists() for p in files):
    raise SystemExit('Run python scripts/download.py first.')
db = ROOT/'data/analytics.duckdb'
con = duckdb.connect(str(db))
con.execute('SET threads=4')
select = '''SELECT
 TRY_STRPTIME("Timestamp",'%d/%m/%Y %H:%M:%S') event_time,
 TRY_CAST("Dst Port" AS INTEGER) dst_port,
 TRY_CAST("Protocol" AS INTEGER) protocol,
 TRY_CAST("Flow Duration" AS DOUBLE)/1000000.0 duration_s,
 TRY_CAST("Tot Fwd Pkts" AS DOUBLE) fwd_pkts,
 TRY_CAST("Tot Bwd Pkts" AS DOUBLE) bwd_pkts,
 TRY_CAST("TotLen Fwd Pkts" AS DOUBLE) fwd_bytes,
 TRY_CAST("TotLen Bwd Pkts" AS DOUBLE) bwd_bytes,
 TRY_CAST("Flow Byts/s" AS DOUBLE) bytes_per_s,
 TRY_CAST("Flow Pkts/s" AS DOUBLE) pkts_per_s,
 TRY_CAST("SYN Flag Cnt" AS INTEGER) syn_flags,
 TRY_CAST("ACK Flag Cnt" AS INTEGER) ack_flags,
 "Label" attack_label,
 ? source_day
 FROM read_csv_auto(?, all_varchar=true, ignore_errors=true)
 WHERE "Label" <> 'Label'
 AND TRY_STRPTIME("Timestamp",'%d/%m/%Y %H:%M:%S') >= TIMESTAMP '2018-02-01'
 AND TRY_STRPTIME("Timestamp",'%d/%m/%Y %H:%M:%S') < TIMESTAMP '2018-04-01' '''
for i,file in enumerate(files):
    stmt = ('CREATE OR REPLACE TABLE flows AS ' if i==0 else 'INSERT INTO flows ')+select
    con.execute(stmt,[file.stem,str(file)])
con.execute('''CREATE OR REPLACE VIEW flow_enriched AS SELECT *,
 attack_label <> 'Benign' is_attack,
 fwd_bytes+bwd_bytes total_bytes,
 (fwd_bytes+1)/(bwd_bytes+1) upload_download_ratio,
 DATE_TRUNC('hour',event_time) hour_start
 FROM flows''')
count,attack = con.execute('SELECT COUNT(*),SUM(is_attack::INT) FROM flow_enriched').fetchone()
assert count > 1000000 and 0 < attack < count, (count,attack)
print(f'{count:,} flows; {attack:,} labeled attacks; database: {db}')
con.close()
