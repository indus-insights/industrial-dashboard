import streamlit as st
import pandas as pd
import numpy as np
from datetime import timedelta

st.set_page_config(
    page_title="Dashboard Journalier", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #ffffff;
}
[data-testid="stHeader"] {
    background-color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    daily = pd.read_excel('daily_dashboard1.xlsx', sheet_name='KPI_Daily')
    weekly = pd.read_excel('daily_dashboard1.xlsx', sheet_name='KPI_Weekly')
    soll = pd.read_excel('daily_dashboard1.xlsx', sheet_name='SOLL')
    actions = pd.read_excel('daily_dashboard1.xlsx', sheet_name='Actions')
    daily['Date'] = pd.to_datetime(daily['Date'], format='%d/%m/%Y')
    return daily, weekly, soll, actions

daily_df, weekly_df, soll_df, actions_df = load_data()
last_row = daily_df.iloc[-1]
current_date = last_row['Date']

def get_networkdays(date):
    month_start = date.replace(day=1)
    next_month = month_start.replace(day=28) + timedelta(days=4)
    month_end = next_month - timedelta(days=next_month.day)
    return np.busday_count(month_start.date(), month_end.date())

current_month_data = daily_df[daily_df['Date'].dt.month == current_date.month]
kunde_mist = current_month_data['Kunde_TIST'].sum()
liefer_mist = current_month_data['Liefer_TIST'].sum()
frtx_mist = current_month_data['FRTX_TIST'].sum()
riskhunting_mist = current_month_data['RiskHunting_TIST'].sum()

def get_soll(kpi_name, col_name):
    row = soll_df[soll_df['KPI'] == kpi_name]
    if row.empty:
        return None
    value = row[col_name].values[0]
    return None if pd.isna(value) else value

risk_t_soll = get_soll('RiskHunting', 'T_SOLL')
kunde_m_soll = get_soll('Kundenreklamation', 'M_SOLL')
liefer_m_soll = get_soll('Lieferantenreklamation', 'M_SOLL')
frtx_m_soll = get_soll('FRTX', 'M_SOLL')
cycle_grenze = get_soll('CycleCounting', 'Grenze')
saa_percent_soll = get_soll('SAA', 'Percent_SOLL')
abw_t_soll = get_soll('Abwesenheit', 'T_SOLL')

networkdays_total = get_networkdays(current_date)
kunde_t_soll = kunde_m_soll / networkdays_total if kunde_m_soll else None
liefer_t_soll = liefer_m_soll / networkdays_total if liefer_m_soll else None
frtx_t_soll = frtx_m_soll / networkdays_total if frtx_m_soll else None
risk_m_soll = risk_t_soll * networkdays_total if risk_t_soll else None

risk_m_gap = riskhunting_mist - risk_m_soll if risk_m_soll else None
kunde_m_gap = kunde_mist - kunde_m_soll if kunde_m_soll else None
liefer_m_gap = liefer_mist - liefer_m_soll if liefer_m_soll else None
frtx_m_gap = frtx_mist - frtx_m_soll if frtx_m_soll else None
saa_m_gap = last_row['SAA_MIST'] - saa_percent_soll if saa_percent_soll else None
abw_t_gap = last_row['Abwesenheit_TIST'] - abw_t_soll if abw_t_soll else None

cycle_tist = last_row['CycleCounting_TIST']
if -cycle_grenze <= cycle_tist <= cycle_grenze:
    cycle_t_gap = 0
elif cycle_tist > cycle_grenze:
    cycle_t_gap = cycle_tist - cycle_grenze
else:
    cycle_t_gap = cycle_tist + cycle_grenze

last_week = weekly_df.iloc[-1]
w_total = last_week['WTotal']
w_completed = last_week['WCompleted']
w_gap = w_completed - w_total

st.markdown(f"<h1 style='text-align: center; margin-bottom: 30px; color: #212529;'>{current_date.strftime('%d.%m.%Y')}</h1>", unsafe_allow_html=True)

st.markdown("""
<style>
.kpi-container {
    background: linear-gradient(145deg, #ffffff, #f0f0f0);
    border: 2px solid #e0e0e0;
    border-radius: 20px;
    padding: 25px 15px;
    text-align: center;
    min-height: 340px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 6px 12px rgba(0,0,0,0.08);
}
.kpi-name {
    font-size: 19px;
    font-weight: bold;
    margin-bottom: 12px;
    color: #1a1a1a;
    letter-spacing: 0.3px;
}
.bubble-top {
    background: white;
    border: 5px solid;
    border-radius: 60px;
    padding: 10px 25px;
    display: inline-block;
    font-weight: bold;
    font-size: 15px;
    margin-bottom: 5px;
    box-shadow: 0 3px 6px rgba(0,0,0,0.1);
    position: relative;
    z-index: 2;
    color: #1a1a1a;
}
.bubble-main {
    background-color: #6bde6b;
    border-radius: 50%;
    width: 170px;
    height: 170px;
    margin: -5px auto 0 auto;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 20px;
    color: #1a1a1a;
    box-shadow: 0 8px 16px rgba(0,0,0,0.15);
    position: relative;
    z-index: 1;
}
.bubble-main.red { 
    background-color: #ff6b6b; 
    color: white; 
}
.bubble-bottom {
    background: white;
    border: 5px solid;
    border-radius: 60px;
    padding: 10px 25px;
    display: inline-block;
    font-weight: bold;
    font-size: 15px;
    margin-top: -5px;
    box-shadow: 0 3px 6px rgba(0,0,0,0.1);
    position: relative;
    z-index: 2;
    color: #1a1a1a;
}
.green-border { border-color: #6bde6b; }
.red-border { border-color: #ff6b6b; }
.blue-border { border-color: #5dade2; }
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    risk_tist = last_row['RiskHunting_TIST']
    big_color = '' if risk_tist >= risk_t_soll else 'red'
    small_color = 'green-border' if risk_m_gap >= 0 else 'red-border'
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-name">Risk Hunting</div>
        <div class="bubble-top {small_color}">M-IST: {riskhunting_mist:.0f}</div>
        <div class="bubble-main {big_color}">T-IST: {risk_tist:.0f}</div>
        <div class="bubble-bottom {small_color}">M-GAP: {risk_m_gap:+.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    kunde_tist = last_row['Kunde_TIST']
    big_color = '' if kunde_mist <= kunde_m_soll else 'red'
    top_color = 'green-border' if kunde_tist <= kunde_t_soll else 'red-border'
    bottom_color = 'green-border' if kunde_mist <= kunde_m_soll else 'red-border'
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-name">Kundenreklamation</div>
        <div class="bubble-top {top_color}">T-IST: {kunde_tist:.0f}</div>
        <div class="bubble-main {big_color}">M-IST: {kunde_mist:.0f}</div>
        <div class="bubble-bottom {bottom_color}">M-GAP: {kunde_m_gap:+.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    liefer_tist = last_row['Liefer_TIST']
    big_color = '' if liefer_mist <= liefer_m_soll else 'red'
    top_color = 'green-border' if liefer_tist <= liefer_t_soll else 'red-border'
    bottom_color = 'green-border' if liefer_mist <= liefer_m_soll else 'red-border'
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-name">Lieferantenreklamation</div>
        <div class="bubble-top {top_color}">T-IST: {liefer_tist:.0f}</div>
        <div class="bubble-main {big_color}">M-IST: {liefer_mist:.0f}</div>
        <div class="bubble-bottom {bottom_color}">M-GAP: {liefer_m_gap:+.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    frtx_tist = last_row['FRTX_TIST']
    big_color = '' if frtx_mist <= frtx_m_soll else 'red'
    top_color = 'green-border' if frtx_tist <= frtx_t_soll else 'red-border'
    bottom_color = 'green-border' if frtx_mist <= frtx_m_soll else 'red-border'
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-name">FRTX</div>
        <div class="bubble-top {top_color}">T-IST: {frtx_tist:.0f}</div>
        <div class="bubble-main {big_color}">M-IST: {frtx_mist:.0f}</div>
        <div class="bubble-bottom {bottom_color}">M-GAP: {frtx_m_gap:+.0f}</div>
    </div>
    """, unsafe_allow_html=True)

col5, col6, col7, col8 = st.columns(4)

with col5:
    big_color = '' if cycle_t_gap == 0 else 'red'
    bottom_color = 'green-border' if cycle_t_gap == 0 else 'red-border'
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-name">Cycle Counting</div>
        <div class="bubble-top blue-border">Grenze: ±{cycle_grenze:.0f}€</div>
        <div class="bubble-main {big_color}">T-IST: {cycle_tist:+.0f}€</div>
        <div class="bubble-bottom {bottom_color}">T-GAP: {cycle_t_gap:+.0f}€</div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    big_color = '' if w_completed >= w_total else 'red'
    bottom_color = 'green-border' if w_gap >= 0 else 'red-border'
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-name">Shipment Tracking</div>
        <div class="bubble-top blue-border">W-Total: {w_total:.0f}</div>
        <div class="bubble-main {big_color}">W-Completed: {w_completed:.0f}</div>
        <div class="bubble-bottom {bottom_color}">W-GAP: {w_gap:+.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col7:
    saa_mist = last_row['SAA_MIST']
    big_color = '' if saa_mist >= saa_percent_soll else 'red'
    bottom_color = 'green-border' if saa_m_gap >= 0 else 'red-border'
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-name">SAA</div>
        <div style="height: 62px;"></div>
        <div class="bubble-main {big_color}">M-IST: {saa_mist:.0f}%</div>
        <div class="bubble-bottom {bottom_color}">M-GAP: {saa_m_gap:+.0f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col8:
    abw_tist = last_row['Abwesenheit_TIST']
    big_color = '' if abw_tist <= abw_t_soll else 'red'
    bottom_color = 'green-border' if abw_t_gap <= 0 else 'red-border'
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-name">Abwesenheit</div>
        <div style="height: 62px;"></div>
        <div class="bubble-main {big_color}">T-IST: {abw_tist:.0f}</div>
        <div class="bubble-bottom {bottom_color}">T-GAP: {abw_t_gap:+.0f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
st.subheader("📋 Actions en cours")

def highlight_status(row):
    if row['Status'] == 'Überfällig':
        return ['background-color: #ff6b6b; color: white'] * len(row)
    elif row['Status'] == 'In Progress':
        return ['background-color: #ffd93d; color: black'] * len(row)
    elif row['Status'] == 'Done':
        return ['background-color: #90ee90; color: black'] * len(row)
    return [''] * len(row)

styled_df = actions_df.style.apply(highlight_status, axis=1)
st.dataframe(styled_df, use_container_width=True, hide_index=True)