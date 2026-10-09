"""Write a small synthetic copy of the three source CSVs to data/raw/ for CI.

Same file names and columns as the real CSE-CIC-IDS2018 days, including the quirks the build has
to handle (a repeated header line mid-file, an unparseable row). It checks that every query runs;
it says nothing about the real data.
"""
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw'
COLS = ['Dst Port', 'Protocol', 'Timestamp', 'Flow Duration', 'Tot Fwd Pkts', 'Tot Bwd Pkts',
        'TotLen Fwd Pkts', 'TotLen Bwd Pkts', 'Flow Byts/s', 'Flow Pkts/s', 'SYN Flag Cnt',
        'ACK Flag Cnt', 'Label']
DAYS = {
    'Wednesday-14-02-2018': (datetime(2018, 2, 14), [('FTP-BruteForce', 21), ('SSH-Bruteforce', 22)]),
    'Thursday-01-03-2018': (datetime(2018, 3, 1), [('Infilteration', 8080)]),
    'Friday-02-03-2018': (datetime(2018, 3, 2), [('Bot', 8080)]),
}

random.seed(7)
RAW.mkdir(parents=True, exist_ok=True)
for name, (day, attacks) in DAYS.items():
    with open(RAW / f'{name}.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(COLS)
        for i in range(3000):
            attack = random.random() < 0.3
            label, port = random.choice(attacks) if attack else ('Benign', random.choice([53, 80, 443, 3389]))
            dur_us = random.randint(10, 5_000_000)
            fwd, bwd = random.randint(1, 40), random.randint(0, 40)
            fb, bb = fwd * random.randint(40, 1500), bwd * random.randint(40, 1500)
            # attacks arrive in a burst, as in the real scenarios; benign traffic spreads over the day
            ts = day + timedelta(seconds=36_000 + random.randint(0, 7_199) if attack else random.randint(0, 86_399))
            w.writerow([port, 6, ts.strftime('%d/%m/%Y %H:%M:%S'), dur_us, fwd, bwd, fb, bb,
                        (fb + bb) / (dur_us / 1e6), (fwd + bwd) / (dur_us / 1e6),
                        int(attack or random.random() < 0.1), random.randint(0, 1), label])
            if i == 1500:
                w.writerow(COLS)  # the real files repeat their header
        w.writerow(['x', 'x', 'not a time'] + ['x'] * 9 + ['Benign'])
print(f'fixture: {len(DAYS)} files in {RAW}')
