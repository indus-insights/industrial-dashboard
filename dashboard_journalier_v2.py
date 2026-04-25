import streamlit as st
import pandas as pd
import numpy as np
from datetime import timedelta
import base64
import os

st.set_page_config(page_title="Production Dashboard", layout="wide", initial_sidebar_state="collapsed")

# Dictionnaire de traductions
TRANSLATIONS = {
    'en': {
        'title': 'DAILY PRODUCTION DASHBOARD',
        'quality': '🎯 QUALITY & COMPLAINTS',
        'safety': '🛡️ SAFETY, LOGISTICS & PERFORMANCE',
        'actions': '📋 OPEN ACTIONS',
        'absences': '👥 ABSENCES',
        'customer_complaints': 'CUSTOMER COMPLAINTS',
        'supplier_complaints': 'SUPPLIER COMPLAINTS',
        'risk_hunting': 'RISK HUNTING',
        'inventory': 'INVENTORY (CYCLE COUNTING)',
        'shipments': 'SHIPMENTS',
        'saa': 'SAA (STANDARD WORK)',
        'of': 'of',
        'monthly_max': 'monthly max',
        'today': 'TODAY',
        'gap': 'GAP',
        'risks_identified': 'risks identified',
        'target': 'target',
        'day': 'day',
        'this_month': 'THIS MONTH',
        'vs_target': 'VS TARGET',
        'variance': 'variance',
        'limit': 'limit',
        'excess': 'EXCESS',
        'week': 'Week',
        'deliveries_completed': 'deliveries completed',
        'compliance': 'compliance',
        'absences_today': 'absences today'
    },
    'de': {
        'title': 'TÄGLICHES PRODUKTIONS-DASHBOARD',
        'quality': '🎯 QUALITÄT & REKLAMATIONEN',
        'safety': '🛡️ SICHERHEIT, LOGISTIK & LEISTUNG',
        'actions': '📋 OFFENE MASSNAHMEN',
        'absences': '👥 ABWESENHEITEN',
        'customer_complaints': 'KUNDENREKLAMATIONEN',
        'supplier_complaints': 'LIEFERANTENREKLAMATIONEN',
        'risk_hunting': 'RISK HUNTING',
        'inventory': 'INVENTUR (CYCLE COUNTING)',
        'shipments': 'LIEFERUNGEN',
        'saa': 'SAA (STANDARDARBEIT)',
        'of': 'von',
        'monthly_max': 'monatl. Max',
        'today': 'HEUTE',
        'gap': 'ABWEICHUNG',
        'risks_identified': 'Risiken identifiziert',
        'target': 'Ziel',
        'day': 'Tag',
        'this_month': 'DIESEN MONAT',
        'vs_target': 'VS ZIEL',
        'variance': 'Abweichung',
        'limit': 'Grenze',
        'excess': 'ÜBERSCHUSS',
        'week': 'Woche',
        'deliveries_completed': 'Lieferungen abgeschlossen',
        'compliance': 'Einhaltung',
        'absences_today': 'Abwesenheiten heute'
    }
}

# CSS Global
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { 
    background: linear-gradient(135deg, #fff5f5 0%, #ffe5e5 100%); 
}
[data-testid="stHeader"] { 
    background-color: transparent;
    display: none;
}
.main {
    padding-top: 0rem !important;
}
.block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 1rem !important;
}
.main-header {
    text-align: center;
    margin: 0px 0 8px 0;
}
.dashboard-title {
    font-size: 32px;
    font-weight: 800;
    color: #c62828;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.15);
}
.dashboard-date {
    font-size: 44px;
    font-weight: 900;
    color: #b71c1c;
    margin-top: 0px;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.2);
}
.section-header {
    font-size: 14px;
    font-weight: 700;
    color: #1a237e;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin: 8px 0 8px 0;
    padding: 6px 10px;
    background: rgba(255,255,255,0.95);
    border-radius: 6px;
    display: inline-block;
}
.metric-card {
    background: white;
    border-radius: 12px;
    padding: 16px;
    box-shadow: 0 3px 10px rgba(0,0,0,0.2);
    transition: transform 0.2s;
    height: 100%;
}
.metric-card:hover { transform: translateY(-3px); box-shadow: 0 6px 16px rgba(0,0,0,0.3); }
.metric-header {
    font-size: 13px;
    font-weight: 700;
    color: #c62828;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 10px;
}
.metric-value {
    font-size: 46px;
    font-weight: 800;
    line-height: 1;
    margin: 5px 0;
}
.metric-value.green { color: #2e7d32; }
.metric-value.red { color: #c62828; }
.metric-label {
    font-size: 12px;
    color: #616161;
    font-weight: 500;
}
.metric-sub {
    display: flex;
    justify-content: space-around;
    margin-top: 12px;
    padding-top: 12px;
    border-top: 2px solid #e0e0e0;
}
.metric-sub-item {
    text-align: center;
    flex: 1;
}
.metric-sub-value {
    font-size: 20px;
    font-weight: 700;
    color: #424242;
}
.metric-sub-label {
    font-size: 10px;
    color: #757575;
    text-transform: uppercase;
    margin-top: 2px;
    font-weight: 600;
}
.divider { 
    height: 1px; 
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent); 
    margin: 18px 0; 
}
</style>
""", unsafe_allow_html=True)

# Gestion de la langue
if 'language' not in st.session_state:
    st.session_state.language = 'en'

# Récupérer les traductions
t = TRANSLATIONS[st.session_state.language]

# Logo Nexans fixe en haut à droite
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_base64 = get_base64_image("nexans_logo.png")

st.markdown(f"""
<style>
.logo-container {{
    position: fixed;
    top: 20px;
    right: 30px;
    z-index: 1000;
}}
.logo-container img {{
    height: 40px;
    filter: drop-shadow(2px 2px 6px rgba(0,0,0,0.25));
}}
</style>
<div class="logo-container">
    <img src="data:image/png;base64,{logo_base64}" alt="Nexans">
</div>
""", unsafe_allow_html=True)

# Switch de langue fixe en haut à gauche - VERSION FINALE QUI MARCHE
st.markdown(f"""
<style>
.language-selector {{
    position: fixed;
    top: 20px;
    left: 20px;
    z-index: 1000;
    background: white;
    border-radius: 25px;
    padding: 6px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    display: flex;
    gap: 4px;
}}
.lang-option {{
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 15px;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s;
    user-select: none;
    text-decoration: none;
    display: block;
}}
.lang-option.inactive {{
    color: #999;
    background: transparent;
}}
.lang-option.active {{
    color: white;
    background: #c62828;
}}
.lang-option:hover {{
    transform: scale(1.05);
}}
</style>
<div class="language-selector">
    <a href="?lang=en" class="lang-option {'active' if st.session_state.language == 'en' else 'inactive'}">
        EN
    </a>
    <a href="?lang=de" class="lang-option {'active' if st.session_state.language == 'de' else 'inactive'}">
        DE
    </a>
</div>
""", unsafe_allow_html=True)

# Gestion du changement de langue via URL
params = st.query_params
if 'lang' in params:
    new_lang = params['lang']
    if new_lang in ['en', 'de'] and new_lang != st.session_state.language:
        st.session_state.language = new_lang
        # Nettoyer les query params et recharger
        st.query_params.clear()
        st.rerun()

# Chargement des données
file_mod_time = os.path.getmtime('daily_dashboard1.xlsx')

@st.cache_data
def load_data(mod_time):
    daily = pd.read_excel('daily_dashboard1.xlsx', sheet_name='KPI_Daily')
    weekly = pd.read_excel('daily_dashboard1.xlsx', sheet_name='KPI_Weekly')
    soll = pd.read_excel('daily_dashboard1.xlsx', sheet_name='SOLL')
    actions = pd.read_excel('daily_dashboard1.xlsx', sheet_name='Actions')
    daily['Date'] = pd.to_datetime(daily['Date'], format='%d/%m/%Y')
    return daily, weekly, soll, actions

daily_df, weekly_df, soll_df, actions_df = load_data(file_mod_time)
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
kunde_t_soll = kunde_m_soll / networkdays_total
liefer_t_soll = liefer_m_soll / networkdays_total
frtx_t_soll = frtx_m_soll / networkdays_total
risk_m_soll = risk_t_soll * networkdays_total

risk_m_gap = riskhunting_mist - risk_m_soll
kunde_m_gap = kunde_mist - kunde_m_soll
liefer_m_gap = liefer_mist - liefer_m_soll
frtx_m_gap = frtx_mist - frtx_m_soll
saa_m_gap = last_row['SAA_MIST'] - saa_percent_soll
abw_t_gap = last_row['Abwesenheit_TIST'] - abw_t_soll

cycle_tist = last_row['CycleCounting_TIST']
if -cycle_grenze <= cycle_tist <= cycle_grenze:
    cycle_t_gap = 0
elif cycle_tist > cycle_grenze:
    cycle_t_gap = cycle_tist - cycle_grenze
else:
    cycle_t_gap = cycle_tist + cycle_grenze

last_week = weekly_df.iloc[-1]
w_gap = last_week['WCompleted'] - last_week['WTotal']

st.markdown(f"""
<div class='main-header'>
    <div class='dashboard-title'>{t['title']}</div>
    <div class='dashboard-date'>{current_date.strftime('%d.%m.%Y')}</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"<div class='section-header'>{t['quality']}</div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    color = 'green' if kunde_mist <= kunde_m_soll else 'red'
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">{t['customer_complaints']}</div>
        <div class="metric-value {color}">{kunde_mist:.0f}</div>
        <div class="metric-label">{t['of']} {kunde_m_soll:.0f} {t['monthly_max']}</div>
        <div class="metric-sub">
            <div class="metric-sub-item">
                <div class="metric-sub-value">{last_row['Kunde_TIST']:.0f}</div>
                <div class="metric-sub-label">{t['today']}</div>
            </div>
            <div class="metric-sub-item">
                <div class="metric-sub-value">{kunde_m_gap:+.0f}</div>
                <div class="metric-sub-label">{t['gap']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    color = 'green' if liefer_mist <= liefer_m_soll else 'red'
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">{t['supplier_complaints']}</div>
        <div class="metric-value {color}">{liefer_mist:.0f}</div>
        <div class="metric-label">{t['of']} {liefer_m_soll:.0f} {t['monthly_max']}</div>
        <div class="metric-sub">
            <div class="metric-sub-item">
                <div class="metric-sub-value">{last_row['Liefer_TIST']:.0f}</div>
                <div class="metric-sub-label">{t['today']}</div>
            </div>
            <div class="metric-sub-item">
                <div class="metric-sub-value">{liefer_m_gap:+.0f}</div>
                <div class="metric-sub-label">{t['gap']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    color = 'green' if frtx_mist <= frtx_m_soll else 'red'
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">FRTX</div>
        <div class="metric-value {color}">{frtx_mist:.0f}</div>
        <div class="metric-label">{t['of']} {frtx_m_soll:.0f} {t['monthly_max']}</div>
        <div class="metric-sub">
            <div class="metric-sub-item">
                <div class="metric-sub-value">{last_row['FRTX_TIST']:.0f}</div>
                <div class="metric-sub-label">{t['today']}</div>
            </div>
            <div class="metric-sub-item">
                <div class="metric-sub-value">{frtx_m_gap:+.0f}</div>
                <div class="metric-sub-label">{t['gap']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

st.markdown(f"<div class='section-header'>{t['safety']}</div>", unsafe_allow_html=True)
col4, col5, col6, col7 = st.columns(4)

with col4:
    color = 'green' if last_row['RiskHunting_TIST'] >= risk_t_soll else 'red'
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">{t['risk_hunting']}</div>
        <div class="metric-value {color}">{last_row['RiskHunting_TIST']:.0f}</div>
        <div class="metric-label">{t['risks_identified']} ({t['target']}: {risk_t_soll:.0f}/{t['day']})</div>
        <div class="metric-sub">
            <div class="metric-sub-item">
                <div class="metric-sub-value">{riskhunting_mist:.0f}</div>
                <div class="metric-sub-label">{t['this_month']}</div>
            </div>
            <div class="metric-sub-item">
                <div class="metric-sub-value">{risk_m_gap:+.0f}</div>
                <div class="metric-sub-label">{t['vs_target']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    color = 'green' if cycle_t_gap == 0 else 'red'
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">{t['inventory']}</div>
        <div class="metric-value {color}">{cycle_tist:+.0f}€</div>
        <div class="metric-label">{t['variance']} ({t['limit']}: ±{cycle_grenze:.0f}€)</div>
        <div class="metric-sub">
            <div class="metric-sub-item">
                <div class="metric-sub-value">{cycle_t_gap:+.0f}€</div>
                <div class="metric-sub-label">{t['excess']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    color = 'green' if last_week['WCompleted'] >= last_week['WTotal'] else 'red'
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">{t['shipments']} ({t['week']} {last_week['Week']:.0f})</div>
        <div class="metric-value {color}">{last_week['WCompleted']:.0f}/{last_week['WTotal']:.0f}</div>
        <div class="metric-label">{t['deliveries_completed']}</div>
        <div class="metric-sub">
            <div class="metric-sub-item">
                <div class="metric-sub-value">{w_gap:+.0f}</div>
                <div class="metric-sub-label">{t['gap']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col7:
    color = 'green' if last_row['SAA_MIST'] >= saa_percent_soll else 'red'
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-header">{t['saa']}</div>
        <div class="metric-value {color}">{last_row['SAA_MIST']:.0f}%</div>
        <div class="metric-label">{t['compliance']} ({t['target']}: {saa_percent_soll:.0f}%)</div>
        <div class="metric-sub">
            <div class="metric-sub-item">
                <div class="metric-sub-value">{saa_m_gap:+.0f}%</div>
                <div class="metric-sub-label">{t['vs_target']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

col8, col9 = st.columns([3, 1])

with col8:
    st.markdown(f"<div class='section-header'>{t['actions']}</div>", unsafe_allow_html=True)
    
    def highlight_status(row):
        if row['Status'] == 'Überfällig':
            return ['background-color: #c62828; color: white; font-weight: bold'] * len(row)
        elif row['Status'] == 'In Progress':
            return ['background-color: #f57c00; color: white'] * len(row)
        elif row['Status'] == 'Done':
            return ['background-color: #2e7d32; color: white'] * len(row)
        return [''] * len(row)
    
    st.dataframe(
        actions_df.style.apply(highlight_status, axis=1),
        use_container_width=True,
        hide_index=True,
        height=200
    )

with col9:
    st.markdown(f"<div class='section-header'>{t['absences']}</div>", unsafe_allow_html=True)
    color = 'green' if last_row['Abwesenheit_TIST'] <= abw_t_soll else 'red'
    st.markdown(f"""
    <div class="metric-card" style="margin-top: 8px;">
        <div class="metric-value {color}" style="font-size: 56px;">{last_row['Abwesenheit_TIST']:.0f}</div>
        <div class="metric-label" style="font-size: 14px;">{t['absences_today']}</div>
        <div class="metric-sub" style="margin-top: 16px;">
            <div class="metric-sub-item">
                <div class="metric-sub-value">{abw_t_gap:+.0f}</div>
                <div class="metric-sub-label">{t['vs_target']} ({abw_t_soll:.0f})</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
