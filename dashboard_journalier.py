import streamlit as st
import pandas as pd
import numpy as np
from datetime import timedelta
import base64
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Production Dashboard", layout="wide", initial_sidebar_state="collapsed")

# Dictionnaire de traductions
TRANSLATIONS = {
    'en': {
        'title': 'DAILY PRODUCTION DASHBOARD',
        'tab_dashboard': '📊 Dashboard',
        'tab_analytics': '📈 Detailed Analytics',
        'quality_safety': '🎯 QUALITY & SAFETY',
        'logistics': '📦 LOGISTICS & PERFORMANCE',
        'actions': '📋 OPEN ACTIONS',
        'absences': '👥 ABSENCES',
        'customer_complaints': 'CUSTOMER COMPLAINTS',
        'supplier_complaints': 'SUPPLIER COMPLAINTS',
        'risk_hunting': 'RISK HUNTING',
        'frtx': 'FRTX',
        'inventory': 'INVENTORY (CYCLE COUNTING)',
        'shipments': 'SHIPMENTS',
        'saa': 'SAA (STANDARD WORK)',
        'of': 'of',
        'monthly_max': 'monthly max',
        'today': 'TODAY',
        'gap': 'GAP',
        'risks_identified': 'risks identified',
        'incidents': 'incidents',
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
        'absences_today': 'absences today',
        'monthly_evolution': 'Monthly Evolution',
        'daily_trend': 'Daily Trend',
        'cumulative': 'Cumulative',
        'objective': 'Objective',
        'actual': 'Actual',
        'tolerance_zone': 'Tolerance Zone',
        'weekly_completion_rate': 'Weekly Completion Rate',
        'compliance_rate': 'Compliance Rate'
    },
    'de': {
        'title': 'TÄGLICHES PRODUKTIONS-DASHBOARD',
        'tab_dashboard': '📊 Dashboard',
        'tab_analytics': '📈 Detaillierte Analytik',
        'quality_safety': '🎯 QUALITÄT & SICHERHEIT',
        'logistics': '📦 LOGISTIK & LEISTUNG',
        'actions': '📋 OFFENE MASSNAHMEN',
        'absences': '👥 ABWESENHEITEN',
        'customer_complaints': 'KUNDENREKLAMATIONEN',
        'supplier_complaints': 'LIEFERANTENREKLAMATIONEN',
        'risk_hunting': 'RISK HUNTING',
        'frtx': 'FRTX',
        'inventory': 'INVENTUR (CYCLE COUNTING)',
        'shipments': 'LIEFERUNGEN',
        'saa': 'SAA (STANDARDARBEIT)',
        'of': 'von',
        'monthly_max': 'monatl. Max',
        'today': 'HEUTE',
        'gap': 'ABWEICHUNG',
        'risks_identified': 'Risiken identifiziert',
        'incidents': 'Vorfälle',
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
        'absences_today': 'Abwesenheiten heute',
        'monthly_evolution': 'Monatliche Entwicklung',
        'daily_trend': 'Täglicher Trend',
        'cumulative': 'Kumulativ',
        'objective': 'Ziel',
        'actual': 'Ist',
        'tolerance_zone': 'Toleranzbereich',
        'weekly_completion_rate': 'Wöchentliche Abschlussrate',
        'compliance_rate': 'Einhaltungsrate'
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
    border-left: 6px solid transparent;
}
.metric-card.status-good {
    border-left-color: #2e7d32 !important;
}
.metric-card.status-bad {
    border-left-color: #c62828 !important;
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
/* Style des onglets */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: transparent;
}
.stTabs [data-baseweb="tab"] {
    background-color: white;
    border-radius: 8px 8px 0 0;
    padding: 12px 24px;
    font-weight: 700;
    color: #666;
    border: none;
}
.stTabs [aria-selected="true"] {
    background-color: white;
    color: #c62828;
    border-bottom: 3px solid #c62828;
}
</style>
""", unsafe_allow_html=True)

# Gestion de la langue
if 'language' not in st.session_state:
    st.session_state.language = 'en'

t = TRANSLATIONS[st.session_state.language]

# Logo Nexans
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

# Switch de langue
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
    pointer-events: none;
}}
.lang-option.inactive:hover {{
    background: #f5f5f5;
    transform: scale(1.05);
}}
</style>
<div class="language-selector">
    <a href="?lang=en" class="lang-option {'active' if st.session_state.language == 'en' else 'inactive'}">EN</a>
    <a href="?lang=de" class="lang-option {'active' if st.session_state.language == 'de' else 'inactive'}">DE</a>
</div>
""", unsafe_allow_html=True)

params = st.query_params
if 'lang' in params:
    new_lang = params['lang']
    if new_lang in ['en', 'de'] and new_lang != st.session_state.language:
        st.session_state.language = new_lang
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

# Titre principal
st.markdown(f"""
<div class='main-header'>
    <div class='dashboard-title'>{t['title']}</div>
    <div class='dashboard-date'>{current_date.strftime('%d.%m.%Y')}</div>
</div>
""", unsafe_allow_html=True)

# ONGLETS
tab1, tab2 = st.tabs([t['tab_dashboard'], t['tab_analytics']])

# ============================================
# ONGLET 1: DASHBOARD
# ============================================
with tab1:
    # LIGNE 1: 4 KPIs sur une ligne (Quality + Safety)
    st.markdown(f"<div class='section-header'>{t['quality_safety']}</div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    # Customer Complaints
    with col1:
        color = 'green' if kunde_mist <= kunde_m_soll else 'red'
        st.markdown(f"""
        <div class="metric-card status-{'good' if condition else 'bad'}">
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
    
    # Supplier Complaints
    with col2:
        color = 'green' if liefer_mist <= liefer_m_soll else 'red'
        st.markdown(f"""
        <div class="metric-card status-{'good' if condition else 'bad'}">
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
    
    # Risk Hunting
    with col3:
        color = 'green' if last_row['RiskHunting_TIST'] >= risk_t_soll else 'red'
        st.markdown(f"""
        <div class="metric-card status-{'good' if condition else 'bad'}">
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
    
    # FRTX
    with col4:
        color = 'green' if frtx_mist <= frtx_m_soll else 'red'
        st.markdown(f"""
        <div class="metric-card status-{'good' if condition else 'bad'}">
            <div class="metric-header">{t['frtx']}</div>
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
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # SECTION 3: LOGISTICS & PERFORMANCE
    st.markdown(f"<div class='section-header'>{t['logistics']}</div>", unsafe_allow_html=True)
    col5, col6, col7 = st.columns(3)
    
    with col5:
        color = 'green' if cycle_t_gap == 0 else 'red'
        st.markdown(f"""
        <div class="metric-card status-{'good' if condition else 'bad'}">
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
        <div class="metric-card status-{'good' if condition else 'bad'}">
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
        <div class="metric-card status-{'good' if condition else 'bad'}">
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
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # SECTION 4: ACTIONS & ABSENCES
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
        <div class="metric-card" style="margin-top: 0px;">
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

# ============================================
# ONGLET 2: DETAILED ANALYTICS
# ============================================
with tab2:
    st.markdown("### " + t['monthly_evolution'])
    
    # Préparer les données cumulatives
    current_month_data = current_month_data.copy()
    current_month_data['Kunde_Cumul'] = current_month_data['Kunde_TIST'].cumsum()
    current_month_data['Liefer_Cumul'] = current_month_data['Liefer_TIST'].cumsum()
    current_month_data['FRTX_Cumul'] = current_month_data['FRTX_TIST'].cumsum()
    current_month_data['RiskHunting_Cumul'] = current_month_data['RiskHunting_TIST'].cumsum()
    
    # SECTION 1: QUALITY COMPLAINTS
    st.markdown(f"<div class='section-header'>{t['quality']}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Customer Complaints
        fig_kunde = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Barres journalières
        fig_kunde.add_trace(
            go.Bar(
                x=current_month_data['Date'],
                y=current_month_data['Kunde_TIST'],
                name=t['daily_trend'],
                marker_color='#ffcdd2',
                opacity=0.6
            ),
            secondary_y=False
        )
        
        # Ligne cumulative
        fig_kunde.add_trace(
            go.Scatter(
                x=current_month_data['Date'],
                y=current_month_data['Kunde_Cumul'],
                name=t['cumulative'],
                line=dict(color='#c62828', width=3),
                mode='lines+markers'
            ),
            secondary_y=True
        )
        
        # Ligne objectif
        fig_kunde.add_trace(
            go.Scatter(
                x=current_month_data['Date'],
                y=[kunde_m_soll] * len(current_month_data),
                name=t['objective'],
                line=dict(color='#2e7d32', width=2, dash='dash'),
                mode='lines'
            ),
            secondary_y=True
        )
        
        fig_kunde.update_layout(
            title=t['customer_complaints'],
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=350,
            margin=dict(l=10, r=10, t=40, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            font=dict(size=11)
        )
        
        fig_kunde.update_yaxes(title_text=t['daily_trend'], secondary_y=False, showgrid=True, gridcolor='#f0f0f0')
        fig_kunde.update_yaxes(title_text=t['cumulative'], secondary_y=True, showgrid=False)
        fig_kunde.update_xaxes(showgrid=False)
        
        st.plotly_chart(fig_kunde, use_container_width=True)
    
    with col2:
        # Supplier Complaints
        fig_liefer = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_liefer.add_trace(
            go.Bar(
                x=current_month_data['Date'],
                y=current_month_data['Liefer_TIST'],
                name=t['daily_trend'],
                marker_color='#ffcdd2',
                opacity=0.6
            ),
            secondary_y=False
        )
        
        fig_liefer.add_trace(
            go.Scatter(
                x=current_month_data['Date'],
                y=current_month_data['Liefer_Cumul'],
                name=t['cumulative'],
                line=dict(color='#c62828', width=3),
                mode='lines+markers'
            ),
            secondary_y=True
        )
        
        fig_liefer.add_trace(
            go.Scatter(
                x=current_month_data['Date'],
                y=[liefer_m_soll] * len(current_month_data),
                name=t['objective'],
                line=dict(color='#2e7d32', width=2, dash='dash'),
                mode='lines'
            ),
            secondary_y=True
        )
        
        fig_liefer.update_layout(
            title=t['supplier_complaints'],
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=350,
            margin=dict(l=10, r=10, t=40, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            font=dict(size=11)
        )
        
        fig_liefer.update_yaxes(title_text=t['daily_trend'], secondary_y=False, showgrid=True, gridcolor='#f0f0f0')
        fig_liefer.update_yaxes(title_text=t['cumulative'], secondary_y=True, showgrid=False)
        fig_liefer.update_xaxes(showgrid=False)
        
        st.plotly_chart(fig_liefer, use_container_width=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # SECTION 2: SAFETY & INCIDENTS
    st.markdown(f"<div class='section-header'>{t['safety']}</div>", unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Risk Hunting
        fig_risk = go.Figure()
        
        fig_risk.add_trace(
            go.Bar(
                x=current_month_data['Date'],
                y=current_month_data['RiskHunting_TIST'],
                name=t['daily_trend'],
                marker_color='#a5d6a7',
                text=current_month_data['RiskHunting_TIST'],
                textposition='outside'
            )
        )
        
        fig_risk.add_trace(
            go.Scatter(
                x=current_month_data['Date'],
                y=[risk_t_soll] * len(current_month_data),
                name=t['objective'],
                line=dict(color='#2e7d32', width=2, dash='dash'),
                mode='lines'
            )
        )
        
        fig_risk.update_layout(
            title=t['risk_hunting'],
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=350,
            margin=dict(l=10, r=10, t=40, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            font=dict(size=11),
            yaxis_title=t['risks_identified']
        )
        
        fig_risk.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
        fig_risk.update_xaxes(showgrid=False)
        
        st.plotly_chart(fig_risk, use_container_width=True)
    
    with col4:
        # FRTX
        fig_frtx = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_frtx.add_trace(
            go.Bar(
                x=current_month_data['Date'],
                y=current_month_data['FRTX_TIST'],
                name=t['daily_trend'],
                marker_color='#ffcdd2',
                opacity=0.6
            ),
            secondary_y=False
        )
        
        fig_frtx.add_trace(
            go.Scatter(
                x=current_month_data['Date'],
                y=current_month_data['FRTX_Cumul'],
                name=t['cumulative'],
                line=dict(color='#c62828', width=3),
                mode='lines+markers'
            ),
            secondary_y=True
        )
        
        fig_frtx.add_trace(
            go.Scatter(
                x=current_month_data['Date'],
                y=[frtx_m_soll] * len(current_month_data),
                name=t['objective'],
                line=dict(color='#2e7d32', width=2, dash='dash'),
                mode='lines'
            ),
            secondary_y=True
        )
        
        fig_frtx.update_layout(
            title=t['frtx'],
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=350,
            margin=dict(l=10, r=10, t=40, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            font=dict(size=11)
        )
        
        fig_frtx.update_yaxes(title_text=t['daily_trend'], secondary_y=False, showgrid=True, gridcolor='#f0f0f0')
        fig_frtx.update_yaxes(title_text=t['cumulative'], secondary_y=True, showgrid=False)
        fig_frtx.update_xaxes(showgrid=False)
        
        st.plotly_chart(fig_frtx, use_container_width=True)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    # SECTION 3: LOGISTICS & PERFORMANCE
    st.markdown(f"<div class='section-header'>{t['logistics']}</div>", unsafe_allow_html=True)
    
    col5, col6, col7 = st.columns(3)
    
    with col5:
        # Cycle Counting
        fig_cycle = go.Figure()
        
        fig_cycle.add_trace(
            go.Scatter(
                x=current_month_data['Date'],
                y=current_month_data['CycleCounting_TIST'],
                name=t['variance'],
                line=dict(color='#c62828', width=3),
                mode='lines+markers',
                fill='tonexty',
                fillcolor='rgba(198, 40, 40, 0.1)'
            )
        )
        
        # Zone de tolérance
        fig_cycle.add_trace(
            go.Scatter(
                x=current_month_data['Date'],
                y=[cycle_grenze] * len(current_month_data),
                name=f'+{cycle_grenze:.0f}€',
                line=dict(color='#ffa726', width=1, dash='dot'),
                mode='lines'
            )
        )
        
        fig_cycle.add_trace(
            go.Scatter(
                x=current_month_data['Date'],
                y=[-cycle_grenze] * len(current_month_data),
                name=f'-{cycle_grenze:.0f}€',
                line=dict(color='#ffa726', width=1, dash='dot'),
                mode='lines',
                fill='tonexty',
                fillcolor='rgba(102, 187, 106, 0.1)'
            )
        )
        
        fig_cycle.update_layout(
            title=t['inventory'],
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=350,
            margin=dict(l=10, r=10, t=40, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            font=dict(size=11),
            yaxis_title='€'
        )
        
        fig_cycle.update_yaxes(showgrid=True, gridcolor='#f0f0f0', zeroline=True, zerolinecolor='#666')
        fig_cycle.update_xaxes(showgrid=False)
        
        st.plotly_chart(fig_cycle, use_container_width=True)
    
    with col6:
        # SAA Compliance
        fig_saa = go.Figure()
        
        fig_saa.add_trace(
            go.Scatter(
                x=current_month_data['Date'],
                y=current_month_data['SAA_MIST'],
                name=t['compliance_rate'],
                line=dict(color='#2e7d32', width=3),
                mode='lines+markers',
                fill='tozeroy',
                fillcolor='rgba(46, 125, 50, 0.1)'
            )
        )
        
        fig_saa.add_trace(
            go.Scatter(
                x=current_month_data['Date'],
                y=[saa_percent_soll] * len(current_month_data),
                name=t['objective'],
                line=dict(color='#c62828', width=2, dash='dash'),
                mode='lines'
            )
        )
        
        fig_saa.update_layout(
            title=t['saa'],
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=350,
            margin=dict(l=10, r=10, t=40, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            font=dict(size=11),
            yaxis_title='%',
            yaxis=dict(range=[80, 100])
        )
        
        fig_saa.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
        fig_saa.update_xaxes(showgrid=False)
        
        st.plotly_chart(fig_saa, use_container_width=True)
    
    with col7:
        # Absences
        fig_abw = go.Figure()
        
        fig_abw.add_trace(
            go.Bar(
                x=current_month_data['Date'],
                y=current_month_data['Abwesenheit_TIST'],
                name=t['absences_today'],
                marker_color=['#c62828' if x > abw_t_soll else '#66bb6a' for x in current_month_data['Abwesenheit_TIST']],
                text=current_month_data['Abwesenheit_TIST'],
                textposition='outside'
            )
        )
        
        fig_abw.add_trace(
            go.Scatter(
                x=current_month_data['Date'],
                y=[abw_t_soll] * len(current_month_data),
                name=t['objective'],
                line=dict(color='#2e7d32', width=2, dash='dash'),
                mode='lines'
            )
        )
        
        fig_abw.update_layout(
            title=t['absences'],
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=350,
            margin=dict(l=10, r=10, t=40, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            font=dict(size=11),
            yaxis_title=t['absences_today']
        )
        
        fig_abw.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
        fig_abw.update_xaxes(showgrid=False)
        
        st.plotly_chart(fig_abw, use_container_width=True)
