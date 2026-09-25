from pathlib import Path
import duckdb
import plotly.express as px
import streamlit as st

ROOT=Path(__file__).resolve().parent
st.set_page_config(page_title='Network intrusion analytics',layout='wide')
st.title('Network intrusion analytics')
st.caption('CSE-CIC-IDS2018 · three selected flow days · labeled traffic analytics')
db=ROOT/'data/analytics.duckdb'
if not db.exists():
    st.error('Run scripts/download.py and scripts/build_db.py first.')
    st.stop()
con=duckdb.connect(str(db),read_only=True)
days=[r[0] for r in con.execute('SELECT DISTINCT source_day FROM flows ORDER BY 1').fetchall()]
selected=st.sidebar.multiselect('Source days',days,default=days)
if not selected:
    st.warning('Select at least one day.');st.stop()
where='source_day IN ('+','.join(repr(x) for x in selected)+')'
count,attacks=con.execute(f'SELECT COUNT(*),SUM(is_attack::INT) FROM flow_enriched WHERE {where}').fetchone()
classes=con.execute(f'SELECT COUNT(DISTINCT attack_label) FROM flow_enriched WHERE {where}').fetchone()[0]
a,b,c=st.columns(3)
a.metric('Flows',f'{count:,}');b.metric('Labeled attack flows',f'{attacks:,}');c.metric('Labels',classes)
hourly=con.execute(f'''SELECT hour_start,attack_label,COUNT(*) flows FROM flow_enriched
 WHERE {where} GROUP BY 1,2 ORDER BY 1,2''').df()
hourly['hour_label']=hourly['hour_start'].dt.strftime('%b %d %H:%M')
hour_chart=px.bar(hourly,x='hour_label',y='flows',color='attack_label',
 title='Traffic by observed hour and label')
hour_chart.update_xaxes(type='category',tickangle=-45)
st.plotly_chart(hour_chart,use_container_width=True)
left,right=st.columns(2)
mix=con.execute(f'''SELECT attack_label,COUNT(*) flows FROM flow_enriched WHERE {where}
 GROUP BY 1 ORDER BY flows DESC''').df()
left.plotly_chart(px.bar(mix,x='attack_label',y='flows',title='Label distribution'),use_container_width=True)
ports=con.execute(f'''SELECT dst_port,COUNT(*) flows,SUM(is_attack::INT) attacks
 FROM flow_enriched WHERE {where} GROUP BY 1 ORDER BY attacks DESC LIMIT 15''').df()
ports['dst_port']=ports['dst_port'].astype(str)
port_chart=px.bar(ports,x='attacks',y='dst_port',orientation='h',hover_data=['flows'],
 title='Most attacked destination ports')
port_chart.update_yaxes(type='category',categoryorder='total ascending')
right.plotly_chart(port_chart,use_container_width=True)
st.subheader('Attack-class profiles')
profile=con.execute(f'''SELECT attack_label,COUNT(*) flows,
 ROUND(QUANTILE_CONT(duration_s,0.5),3) median_duration_s,
 ROUND(QUANTILE_CONT(total_bytes,0.5),1) median_bytes,
 ROUND(100.0*AVG((syn_flags>0)::INT),2) syn_share_pct
 FROM flow_enriched WHERE {where} GROUP BY 1 ORDER BY flows DESC''').df()
st.dataframe(profile,use_container_width=True,hide_index=True)
st.caption('This selected-day corpus is not a random sample of all CSE-CIC-IDS2018 traffic. Labels come from the source dataset; traffic statistics alone do not prove malicious intent.')
con.close()
