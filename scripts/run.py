from pathlib import Path
import duckdb
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
con = duckdb.connect(str(ROOT / 'data/analytics.duckdb'), read_only=True)
out = ROOT / 'results'
charts = ROOT / 'charts'
out.mkdir(exist_ok=True)
charts.mkdir(exist_ok=True)

def markdown(df):
    cols = [str(c) for c in df.columns]
    rows = [['' if v is None else str(round(v, 4) if isinstance(v, float) else v) for v in row]
            for row in df.itertuples(index=False, name=None)]
    return '| ' + ' | '.join(cols) + ' |\n| ' + ' | '.join(['---']*len(cols)) + ' |\n' + ''.join('| ' + ' | '.join(r) + ' |\n' for r in rows)

for file in sorted((ROOT / 'sql').glob('*.sql')):
    sql = file.read_text()
    title = sql.splitlines()[0].removeprefix('-- ').strip()
    df = con.execute(sql).df()
    df.to_csv(out / f'{file.stem}.csv', index=False)
    (out / f'{file.stem}.md').write_text(f'# {title}\n\n{markdown(df.head(30))}')
    print(file.name, len(df), 'rows')

hourly = con.execute((ROOT/'sql/03_hourly_attack_rate.sql').read_text()).df()
fig,ax=plt.subplots(figsize=(10,4.5))
ax.plot(hourly['hour_start'],hourly['attacks'],color='#dc2626')
ax.set(title='Labeled attack flows by hour',xlabel='Hour',ylabel='Attack flows')
fig.autofmt_xdate();fig.tight_layout();fig.savefig(charts/'attacks_by_hour.png',dpi=160);plt.close(fig)

mix = con.execute((ROOT/'sql/01_attack_mix.sql').read_text()).df()
fig,ax=plt.subplots(figsize=(9,4.5))
ax.bar(mix['attack_label'],mix['flows'],color='#0f766e')
ax.set(title='Traffic by dataset label',xlabel='Label',ylabel='Flows')
ax.tick_params(axis='x',rotation=25);fig.tight_layout();fig.savefig(charts/'label_mix.png',dpi=160);plt.close(fig)
