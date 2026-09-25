from pathlib import Path
from urllib.request import urlretrieve
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
raw = ROOT/'data/raw'
raw.mkdir(parents=True,exist_ok=True)
days = ('Wednesday-14-02-2018','Thursday-01-03-2018','Friday-02-03-2018')
for day in days:
    target = raw/f'{day}.csv'
    key = f'Processed Traffic Data for ML Algorithms/{day}_TrafficForML_CICFlowMeter.csv'
    url = 'https://cse-cic-ids2018.s3.ca-central-1.amazonaws.com/'+quote(key)
    if not target.exists():
        urlretrieve(url,target)
    print(f'{target.name}: {target.stat().st_size:,} bytes')
