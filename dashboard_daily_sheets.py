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
        'absences_today': 'Absences today',
        'monthly_evolution': 'Monthly Evolution',
        'daily_trend': 'Daily Trend',
        'cumulative': 'Cumulative',
        'objective': 'Objective',
        'actual': 'Actual',
        'tolerance_zone': 'Tolerance Zone',
        'weekly_completion_rate': 'Weekly Completion Rate',
        'compliance_rate': 'Compliance Rate',
        'col_theme': 'Theme',
        'col_date': 'Date',
        'col_responsible': 'Responsible',
        'col_action': 'Action',
        'col_deadline': 'Deadline',
        'col_status': 'Status'
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
        'compliance_rate': 'Einhaltungsrate',
        'col_theme': 'Thema',
        'col_date': 'Datum',
        'col_responsible': 'Verantwortlich',
        'col_action': 'Aktion',
        'col_deadline': 'Deadline',
        'col_status': 'Status'
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
    font-size: 36px;
    font-weight: 900;
    color: #c62828;
    letter-spacing: 2px;
    text-transform: uppercase;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.15);
}
.dashboard-date {
    font-size: 16px;
    font-weight: 600;
    color: #666;
    margin-top: 4px;
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
    transition: transform 0.2s, box-shadow 0.2s;
    height: 100%;
    border: 6px solid transparent;
}
.metric-card:hover { 
    transform: translateY(-3px); 
    box-shadow: 0 6px 16px rgba(0,0,0,0.3); 
}
.metric-card.status-good {
    border-color: #2e7d32 !important;
    box-shadow: 0 3px 10px rgba(46, 125, 50, 0.25);
}
.metric-card.status-good:hover {
    box-shadow: 0 6px 16px rgba(46, 125, 50, 0.4);
}
.metric-card.status-bad {
    border-color: #c62828 !important;
    box-shadow: 0 3px 10px rgba(198, 40, 40, 0.25);
}
.metric-card.status-bad:hover {
    box-shadow: 0 6px 16px rgba(198, 40, 40, 0.4);
}
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
/* Boutons invisibles pour les cartes cliquables */
button[kind="secondary"] {
    opacity: 0 !important;
    height: 50px !important;
    background: transparent !important;
    border: none !important;
    cursor: pointer !important;
}
button[kind="secondary"]:hover {
    background: rgba(198, 40, 40, 0.05) !important;
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

# ============================================
# CONNEXION GOOGLE SHEETS
# ============================================
from google.oauth2 import service_account
import gspread

# Connexion à Google Sheets via Service Account
@st.cache_resource
def get_gsheet_client():
    """Créer la connexion au client Google Sheets"""
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ],
    )
    return gspread.authorize(credentials)

# Charger les données depuis Google Sheets
@st.cache_data(ttl=60)
def load_data_from_sheets(_client):
    try:
        # Test 1 : Lister tous les fichiers accessibles
        st.write("📂 Fichiers Google Sheets accessibles :")
        all_files = _client.openall()
        for f in all_files[:5]:  # Affiche les 5 premiers
            st.write(f"- {f.title} (ID: {f.id})")
        
        # Test 2 : Ouvrir par URL
        GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/10h_8rBooLZlS0P7JO24wyQ1-Y_vHe6a1/edit"  # Change ça !
        st.write(f"🔗 Tentative d'ouverture : {GOOGLE_SHEETS_URL}")
        
        spreadsheet = _client.open_by_url(GOOGLE_SHEETS_URL)
        st.success(f"✅ Fichier ouvert : {spreadsheet.title}")
        
        # Test 3 : Lister les feuilles
        st.write("📊 Feuilles disponibles :")
        for sheet in spreadsheet.worksheets():
            st.write(f"- {sheet.title}")
        
        # Test 4 : Lire une feuille
        daily_sheet = spreadsheet.worksheet("KPI_Daily")
        st.write(f"✅ Feuille KPI_Daily trouvée : {daily_sheet.row_count} lignes")
        
        # Test 5 : Récupérer les données
        daily_data = daily_sheet.get_all_records()
        st.write(f"📊 Données : {len(daily_data)} lignes récupérées")
        st.write("Aperçu :", daily_data[:2])
        
        # Si tout fonctionne, convertir
        daily = pd.DataFrame(daily_data)
        st.dataframe(daily.head())
        
        return daily, None, None, None
        
    except Exception as e:
        st.error(f"❌ Erreur : {type(e).__name__}")
        st.error(f"Message : {str(e)}")
        import traceback
        st.code(traceback.format_exc())
        st.stop()

# Initialiser la connexion
gsheet_client = get_gsheet_client()

# Charger les données
daily_df, weekly_df, soll_df, actions_df = load_data_from_sheets(gsheet_client)
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

# Trouver la semaine correspondant à current_date (pas forcément la dernière ligne)
# Calculer le numéro de semaine de current_date
import datetime
current_week_number = current_date.isocalendar()[1]

# Chercher la ligne dans weekly_df qui correspond à cette semaine
matching_weeks = weekly_df[weekly_df['Week'] == current_week_number]

if len(matching_weeks) > 0:
    # Prendre la dernière occurrence si plusieurs (au cas où il y aurait plusieurs années)
    last_week = matching_weeks.iloc[-1]
else:
    # Fallback : prendre la dernière semaine disponible
    last_week = weekly_df.iloc[-1]

w_gap = last_week['WCompleted'] - last_week['WTotal']

# Préparer les données pour les graphiques modaux
current_month_data_modal = current_month_data.copy()
current_month_data_modal['Kunde_Cumul'] = current_month_data_modal['Kunde_TIST'].cumsum()
current_month_data_modal['Liefer_Cumul'] = current_month_data_modal['Liefer_TIST'].cumsum()
current_month_data_modal['FRTX_Cumul'] = current_month_data_modal['FRTX_TIST'].cumsum()
 
# Calculer les dates futures
last_date_modal = current_month_data_modal['Date'].max()
 
if last_date_modal.month == 12:
    month_end_modal = last_date_modal.replace(day=31)
else:
    next_month = last_date_modal.replace(day=28) + timedelta(days=4)
    month_end_modal = next_month - timedelta(days=next_month.day)
 
future_dates_modal = []
current_check = last_date_modal + timedelta(days=1)
 
while len(future_dates_modal) < 3 and current_check <= month_end_modal:
    if current_check.weekday() < 5:
        future_dates_modal.append(current_check)
    current_check += timedelta(days=1)
 
# Créer extended_data
if future_dates_modal:
    future_df_modal = pd.DataFrame({
        'Date': future_dates_modal,
        'Kunde_TIST': [None] * len(future_dates_modal),
        'Liefer_TIST': [None] * len(future_dates_modal),
        'RiskHunting_TIST': [None] * len(future_dates_modal),
        'FRTX_TIST': [None] * len(future_dates_modal),
        'CycleCounting_TIST': [None] * len(future_dates_modal),
        'SAA_MIST': [None] * len(future_dates_modal),
        'Abwesenheit_TIST': [None] * len(future_dates_modal),
        'Kunde_Cumul': [None] * len(future_dates_modal),
        'Liefer_Cumul': [None] * len(future_dates_modal),
        'FRTX_Cumul': [None] * len(future_dates_modal)
    })
    extended_data_modal = pd.concat([current_month_data_modal, future_df_modal], ignore_index=True)
else:
    extended_data_modal = current_month_data_modal
 
# Créer les objectifs cumulatifs
days_so_far = list(range(1, len(current_month_data_modal) + 1))
kunde_cumul_soll_modal = [kunde_t_soll * i for i in days_so_far]
liefer_cumul_soll_modal = [liefer_t_soll * i for i in days_so_far]
 
if future_dates_modal:
    for i in range(len(future_dates_modal)):
        kunde_cumul_soll_modal.append(kunde_t_soll * (len(current_month_data_modal) + i + 1))
        liefer_cumul_soll_modal.append(liefer_t_soll * (len(current_month_data_modal) + i + 1))
 
# ONGLETS

# Préparer les données pour les graphiques modaux
current_month_data_modal = current_month_data.copy()
current_month_data_modal['Kunde_Cumul'] = current_month_data_modal['Kunde_TIST'].cumsum()
current_month_data_modal['Liefer_Cumul'] = current_month_data_modal['Liefer_TIST'].cumsum()
current_month_data_modal['FRTX_Cumul'] = current_month_data_modal['FRTX_TIST'].cumsum()
 
# Calculer les dates futures
last_date_modal = current_month_data_modal['Date'].max()
 
if last_date_modal.month == 12:
    month_end_modal = last_date_modal.replace(day=31)
else:
    next_month = last_date_modal.replace(day=28) + timedelta(days=4)
    month_end_modal = next_month - timedelta(days=next_month.day)
 
future_dates_modal = []
current_check = last_date_modal + timedelta(days=1)
 
while len(future_dates_modal) < 3 and current_check <= month_end_modal:
    if current_check.weekday() < 5:
        future_dates_modal.append(current_check)
    current_check += timedelta(days=1)
 
# Créer extended_data
if future_dates_modal:
    future_df_modal = pd.DataFrame({
        'Date': future_dates_modal,
        'Kunde_TIST': [None] * len(future_dates_modal),
        'Liefer_TIST': [None] * len(future_dates_modal),
        'RiskHunting_TIST': [None] * len(future_dates_modal),
        'FRTX_TIST': [None] * len(future_dates_modal),
        'CycleCounting_TIST': [None] * len(future_dates_modal),
        'SAA_MIST': [None] * len(future_dates_modal),
        'Abwesenheit_TIST': [None] * len(future_dates_modal),
        'Kunde_Cumul': [None] * len(future_dates_modal),
        'Liefer_Cumul': [None] * len(future_dates_modal),
        'FRTX_Cumul': [None] * len(future_dates_modal)
    })
    extended_data_modal = pd.concat([current_month_data_modal, future_df_modal], ignore_index=True)
else:
    extended_data_modal = current_month_data_modal
 
# Créer les objectifs cumulatifs
days_so_far = list(range(1, len(current_month_data_modal) + 1))
kunde_cumul_soll_modal = [kunde_t_soll * i for i in days_so_far]
liefer_cumul_soll_modal = [liefer_t_soll * i for i in days_so_far]
 
if future_dates_modal:
    for i in range(len(future_dates_modal)):
        kunde_cumul_soll_modal.append(kunde_t_soll * (len(current_month_data_modal) + i + 1))
        liefer_cumul_soll_modal.append(liefer_t_soll * (len(current_month_data_modal) + i + 1))
 
 
# ============================================
# FONCTIONS MODALES AVEC @st.dialog
# ============================================
 
@st.dialog(t['customer_complaints'], width="large")
def show_kunde_chart():
    """Modal pour Customer Complaints"""
    fig_kunde = go.Figure()
    
    bar_colors = ['#66bb6a' if val <= soll else '#ef5350' 
                  for val, soll in zip(current_month_data_modal['Kunde_Cumul'], kunde_cumul_soll_modal[:len(current_month_data_modal)])]
    
    fig_kunde.add_trace(
        go.Bar(
            x=current_month_data_modal['Date'],
            y=current_month_data_modal['Kunde_Cumul'],
            name=t['cumulative'],
            marker_color=bar_colors,
            text=current_month_data_modal['Kunde_Cumul'],
            textposition='outside',
            textfont=dict(color='#424242', size=10)
        )
    )
    
    fig_kunde.add_trace(
        go.Scatter(
            x=extended_data_modal['Date'],
            y=kunde_cumul_soll_modal,
            name=t['objective'],
            line=dict(color='#b71c1c', width=3),
            mode='lines'
        )
    )
    
    fig_kunde.update_layout(
        title=dict(text=t['customer_complaints'], font=dict(color='#1a237e', size=16, family='Arial Black')),
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=350,
        margin=dict(l=10, r=10, t=60, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#424242')),
        font=dict(size=11, color='#424242')
    )
    
    fig_kunde.update_yaxes(
        title_text=t['cumulative'], 
        showgrid=True, 
        gridcolor='#f0f0f0', 
        title_font=dict(color='#424242'),
        rangemode='tozero'
    )
    fig_kunde.update_xaxes(
        showgrid=False, 
        tickfont=dict(color='#424242'),
        tickformat='%d/%m',
        dtick=86400000,
        range=[extended_data_modal['Date'].min() - timedelta(hours=12), extended_data_modal['Date'].max() + timedelta(hours=12)]
    )
    
    st.plotly_chart(fig_kunde, use_container_width=True)
 
 
@st.dialog(t['supplier_complaints'], width="large")
def show_liefer_chart():
    """Modal pour Supplier Complaints"""
    fig_liefer = go.Figure()
    
    bar_colors = ['#66bb6a' if val <= soll else '#ef5350' 
                  for val, soll in zip(current_month_data_modal['Liefer_Cumul'], liefer_cumul_soll_modal[:len(current_month_data_modal)])]
    
    fig_liefer.add_trace(
        go.Bar(
            x=current_month_data_modal['Date'],
            y=current_month_data_modal['Liefer_Cumul'],
            name=t['cumulative'],
            marker_color=bar_colors,
            text=current_month_data_modal['Liefer_Cumul'],
            textposition='outside',
            textfont=dict(color='#424242', size=10)
        )
    )
    
    fig_liefer.add_trace(
        go.Scatter(
            x=extended_data_modal['Date'],
            y=liefer_cumul_soll_modal,
            name=t['objective'],
            line=dict(color='#b71c1c', width=3),
            mode='lines'
        )
    )
    
    fig_liefer.update_layout(
        title=dict(text=t['supplier_complaints'], font=dict(color='#1a237e', size=16, family='Arial Black')),
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=350,
        margin=dict(l=10, r=10, t=60, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#424242')),
        font=dict(size=11, color='#424242')
    )
    
    fig_liefer.update_yaxes(
        title_text=t['cumulative'], 
        showgrid=True, 
        gridcolor='#f0f0f0', 
        title_font=dict(color='#424242'),
        rangemode='tozero'
    )
    fig_liefer.update_xaxes(
        showgrid=False, 
        tickfont=dict(color='#424242'),
        tickformat='%d/%m',
        dtick=86400000,
        range=[extended_data_modal['Date'].min() - timedelta(hours=12), extended_data_modal['Date'].max() + timedelta(hours=12)]
    )
    
    st.plotly_chart(fig_liefer, use_container_width=True)
 
 
@st.dialog(t['risk_hunting'], width="large")
def show_risk_chart():
    """Modal pour Risk Hunting"""
    fig_risk = go.Figure()
    
    bar_colors = ['#66bb6a' if val >= risk_t_soll else '#ef5350' for val in current_month_data_modal['RiskHunting_TIST']]
    
    fig_risk.add_trace(
        go.Bar(
            x=current_month_data_modal['Date'],
            y=current_month_data_modal['RiskHunting_TIST'],
            name=t['daily_trend'],
            marker_color=bar_colors,
            text=current_month_data_modal['RiskHunting_TIST'],
            textposition='outside',
            textfont=dict(color='#424242', size=10)
        )
    )
    
    fig_risk.add_trace(
        go.Scatter(
            x=extended_data_modal['Date'],
            y=[risk_t_soll] * len(extended_data_modal),
            name=t['objective'],
            line=dict(color='#b71c1c', width=3),
            mode='lines'
        )
    )
    
    fig_risk.update_layout(
        title=dict(text=t['risk_hunting'], font=dict(color='#1a237e', size=16, family='Arial Black')),
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=350,
        margin=dict(l=10, r=10, t=60, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#424242')),
        font=dict(size=11, color='#424242'),
        yaxis_title=t['risks_identified'],
        yaxis=dict(title_font=dict(color='#424242'), rangemode='tozero')
    )
    
    fig_risk.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    fig_risk.update_xaxes(
        showgrid=False, 
        tickfont=dict(color='#424242'),
        tickformat='%d/%m',
        dtick=86400000,
        range=[extended_data_modal['Date'].min() - timedelta(hours=12), extended_data_modal['Date'].max() + timedelta(hours=12)]
    )
    
    st.plotly_chart(fig_risk, use_container_width=True)
 
 
@st.dialog(t['frtx'], width="large")
def show_frtx_chart():
    """Modal pour FRTX"""
    fig_frtx = go.Figure()
    
    bar_colors = ['#66bb6a' if val == 0 else '#ef5350' for val in current_month_data_modal['FRTX_TIST']]
    
    fig_frtx.add_trace(
        go.Bar(
            x=current_month_data_modal['Date'],
            y=current_month_data_modal['FRTX_TIST'],
            name=t['daily_trend'],
            marker_color=bar_colors,
            text=current_month_data_modal['FRTX_TIST'],
            textposition='outside',
            textfont=dict(color='#424242', size=10)
        )
    )
    
    fig_frtx.add_trace(
        go.Scatter(
            x=extended_data_modal['Date'],
            y=[frtx_t_soll] * len(extended_data_modal),
            name=t['objective'],
            line=dict(color='#b71c1c', width=3),
            mode='lines'
        )
    )
    
    fig_frtx.update_layout(
        title=dict(text=t['frtx'], font=dict(color='#1a237e', size=16, family='Arial Black')),
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=350,
        margin=dict(l=10, r=10, t=60, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#424242')),
        font=dict(size=11, color='#424242')
    )
    
    fig_frtx.update_yaxes(title_text=t['daily_trend'], showgrid=True, gridcolor='#f0f0f0', title_font=dict(color='#424242'), rangemode='tozero')
    fig_frtx.update_xaxes(
        showgrid=False, 
        tickfont=dict(color='#424242'),
        tickformat='%d/%m',
        dtick=86400000,
        range=[extended_data_modal['Date'].min() - timedelta(hours=12), extended_data_modal['Date'].max() + timedelta(hours=12)]
    )
    
    st.plotly_chart(fig_frtx, use_container_width=True)
 
 
@st.dialog(t['inventory'], width="large")
def show_cycle_chart():
    """Modal pour Cycle Counting"""
    fig_cycle = go.Figure()
    
    fig_cycle.add_trace(
        go.Scatter(
            x=current_month_data_modal['Date'],
            y=current_month_data_modal['CycleCounting_TIST'],
            name=t['variance'],
            line=dict(color='#c62828', width=3),
            mode='lines+markers',
            marker=dict(size=6),
            fill='tonexty',
            fillcolor='rgba(198, 40, 40, 0.1)'
        )
    )
    
    fig_cycle.add_trace(
        go.Scatter(
            x=extended_data_modal['Date'],
            y=[cycle_grenze] * len(extended_data_modal),
            name=f'+{cycle_grenze:.0f}€',
            line=dict(color='#ffa726', width=1, dash='dot'),
            mode='lines'
        )
    )
    
    fig_cycle.add_trace(
        go.Scatter(
            x=extended_data_modal['Date'],
            y=[-cycle_grenze] * len(extended_data_modal),
            name=f'-{cycle_grenze:.0f}€',
            line=dict(color='#ffa726', width=1, dash='dot'),
            mode='lines',
            fill='tonexty',
            fillcolor='rgba(102, 187, 106, 0.1)'
        )
    )
    
    fig_cycle.update_layout(
        title=dict(text=t['inventory'], font=dict(color='#1a237e', size=16, family='Arial Black')),
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=350,
        margin=dict(l=10, r=10, t=60, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#424242')),
        font=dict(size=11, color='#424242'),
        yaxis_title='€',
        yaxis=dict(title_font=dict(color='#424242'))
    )
    
    fig_cycle.update_yaxes(showgrid=True, gridcolor='#f0f0f0', zeroline=True, zerolinecolor='#666')
    fig_cycle.update_xaxes(
        showgrid=False, 
        tickfont=dict(color='#424242'),
        tickformat='%d/%m',
        dtick=86400000,
        range=[extended_data_modal['Date'].min() - timedelta(hours=12), extended_data_modal['Date'].max() + timedelta(hours=12)]
    )
    
    st.plotly_chart(fig_cycle, use_container_width=True)
 
 
@st.dialog(t['saa'], width="large")
def show_saa_chart():
    """Modal pour SAA"""
    fig_saa = go.Figure()
    
    fig_saa.add_trace(
        go.Scatter(
            x=current_month_data_modal['Date'],
            y=current_month_data_modal['SAA_MIST'],
            name=t['compliance_rate'],
            line=dict(color='#2e7d32', width=3),
            mode='lines+markers',
            marker=dict(size=6),
            fill='tozeroy',
            fillcolor='rgba(46, 125, 50, 0.1)'
        )
    )
    
    fig_saa.add_trace(
        go.Scatter(
            x=extended_data_modal['Date'],
            y=[saa_percent_soll] * len(extended_data_modal),
            name=t['objective'],
            line=dict(color='#b71c1c', width=3),
            mode='lines'
        )
    )
    
    fig_saa.update_layout(
        title=dict(text=t['saa'], font=dict(color='#1a237e', size=16, family='Arial Black')),
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=350,
        margin=dict(l=10, r=10, t=60, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#424242')),
        font=dict(size=11, color='#424242'),
        yaxis_title='%',
        yaxis=dict(range=[80, 100], title_font=dict(color='#424242'))
    )
    
    fig_saa.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    fig_saa.update_xaxes(
        showgrid=False, 
        tickfont=dict(color='#424242'),
        tickformat='%d/%m',
        dtick=86400000,
        range=[extended_data_modal['Date'].min() - timedelta(hours=12), extended_data_modal['Date'].max() + timedelta(hours=12)]
    )
    
    st.plotly_chart(fig_saa, use_container_width=True)
 
 
@st.dialog(t['absences'], width="large")
def show_abw_chart():
    """Modal pour Absences"""
    fig_abw = go.Figure()
    
    bar_colors = ['#ef5350' if x > abw_t_soll else '#66bb6a' for x in current_month_data_modal['Abwesenheit_TIST']]
    
    fig_abw.add_trace(
        go.Bar(
            x=current_month_data_modal['Date'],
            y=current_month_data_modal['Abwesenheit_TIST'],
            name=t['absences_today'],
            marker_color=bar_colors,
            text=current_month_data_modal['Abwesenheit_TIST'],
            textposition='outside',
            textfont=dict(color='#424242', size=10)
        )
    )
    
    fig_abw.add_trace(
        go.Scatter(
            x=extended_data_modal['Date'],
            y=[abw_t_soll] * len(extended_data_modal),
            name=t['objective'],
            line=dict(color='#b71c1c', width=3),
            mode='lines'
        )
    )
    
    fig_abw.update_layout(
        title=dict(text=t['absences'], font=dict(color='#1a237e', size=16, family='Arial Black')),
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=350,
        margin=dict(l=10, r=10, t=60, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#424242')),
        font=dict(size=11, color='#424242'),
        yaxis_title=t['absences_today'],
        yaxis=dict(title_font=dict(color='#424242'), rangemode='tozero')
    )
    
    fig_abw.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
    fig_abw.update_xaxes(
        showgrid=False, 
        tickfont=dict(color='#424242'),
        tickformat='%d/%m',
        dtick=86400000,
        range=[extended_data_modal['Date'].min() - timedelta(hours=12), extended_data_modal['Date'].max() + timedelta(hours=12)]
    )
    
    st.plotly_chart(fig_abw, use_container_width=True)


@st.dialog(t['shipments'], width="large")
def show_shipments_chart():
    """Modal pour Shipments - Graphique hebdomadaire"""
    fig_ship = go.Figure()
    
    # Extraire les 5 dernières semaines
    recent_weeks = weekly_df.tail(5) if len(weekly_df) >= 5 else weekly_df
    
    # Positions des barres pour chaque semaine
    weeks = recent_weeks['Week'].astype(str)
    x_positions = list(range(len(weeks)))
    
    # Barres: Completed (gauche) et Total (droite)
    bar_width = 0.35
    
    # Barres des shipments réalisés (à gauche, rouge si < total, vert si = total)
    completed = recent_weeks['WCompleted'].values
    total = recent_weeks['WTotal'].values
    bar_colors_completed = ['#66bb6a' if c >= t else '#ef5350' for c, t in zip(completed, total)]
    
    fig_ship.add_trace(
        go.Bar(
            x=[i - bar_width/2 for i in x_positions],
            y=completed,
            name=t['actual'],
            marker_color=bar_colors_completed,
            width=bar_width,
            text=completed,
            textposition='outside',
            textfont=dict(color='#424242', size=10)
        )
    )
    
    # Barres du total attendu (à droite, bleu foncé)
    fig_ship.add_trace(
        go.Bar(
            x=[i + bar_width/2 for i in x_positions],
            y=total,
            name='Total',
            marker_color='#1565c0',
            width=bar_width,
            text=total,
            textposition='outside',
            textfont=dict(color='#424242', size=10)
        )
    )
    
    fig_ship.update_layout(
        title=dict(text=t['shipments'], font=dict(color='#1a237e', size=16, family='Arial Black')),
        xaxis=dict(
            tickmode='array',
            tickvals=x_positions,
            ticktext=[f"{t['week']} {w}" for w in weeks],
            title='',
            tickfont=dict(color='#424242')
        ),
        yaxis=dict(
            title=t['deliveries_completed'],
            title_font=dict(color='#424242'),
            showgrid=True,
            gridcolor='#f0f0f0',
            rangemode='tozero'
        ),
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=350,
        margin=dict(l=10, r=10, t=60, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#424242')),
        font=dict(size=11, color='#424242'),
        barmode='group'
    )
    
    st.plotly_chart(fig_ship, use_container_width=True)


# Titre principal
st.markdown(f"""
<div class='main-header'>
    <div class='dashboard-title'>{t['title']}</div>
    <div class='dashboard-date'>{current_date.strftime('%d.%m.%Y')}</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs([t['tab_dashboard'], t['tab_analytics']])

# ============================================
# ONGLET 1: DASHBOARD AVEC CARTES CLIQUABLES
# ============================================
with tab1:
    # LIGNE 1: 4 KPIs sur une ligne (Quality & Safety)
    st.markdown(f"<div class='section-header'>{t['quality_safety']}</div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    # Customer Complaints
    with col1:
        color = 'green' if kunde_mist <= kunde_m_soll else 'red'
        status_class = 'status-good' if kunde_mist <= kunde_m_soll else 'status-bad'
        
        # Bouton invisible
        clicked = st.button('', key='btn_kunde', help='📊 Cliquer pour voir le graphique détaillé', use_container_width=True, type='secondary')
        
        st.markdown(f"""
        <div class="metric-card {status_class}" style="margin-top: -60px; position: relative; z-index: 1; pointer-events: none;">
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
            <div style="position: absolute; top: 10px; right: 12px; font-size: 18px; opacity: 0.4;">📊</div>
        </div>
        """, unsafe_allow_html=True)
        
        if clicked:
            show_kunde_chart()
    
    # Supplier Complaints
    with col2:
        color = 'green' if liefer_mist <= liefer_m_soll else 'red'
        status_class = 'status-good' if liefer_mist <= liefer_m_soll else 'status-bad'
        
        clicked = st.button('', key='btn_liefer', help='📊 Cliquer pour voir le graphique détaillé', use_container_width=True, type='secondary')
        
        st.markdown(f"""
        <div class="metric-card {status_class}" style="margin-top: -60px; position: relative; z-index: 1; pointer-events: none;">
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
            <div style="position: absolute; top: 10px; right: 12px; font-size: 18px; opacity: 0.4;">📊</div>
        </div>
        """, unsafe_allow_html=True)
        
        if clicked:
            show_liefer_chart()
    
    # Risk Hunting
    with col3:
        color = 'green' if last_row['RiskHunting_TIST'] >= risk_t_soll else 'red'
        status_class = 'status-good' if last_row['RiskHunting_TIST'] >= risk_t_soll else 'status-bad'
        
        clicked = st.button('', key='btn_risk', help='📊 Cliquer pour voir le graphique détaillé', use_container_width=True, type='secondary')
        
        st.markdown(f"""
        <div class="metric-card {status_class}" style="margin-top: -60px; position: relative; z-index: 1; pointer-events: none;">
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
            <div style="position: absolute; top: 10px; right: 12px; font-size: 18px; opacity: 0.4;">📊</div>
        </div>
        """, unsafe_allow_html=True)
        
        if clicked:
            show_risk_chart()
    
    # FRTX
    with col4:
        color = 'green' if frtx_mist <= frtx_m_soll else 'red'
        status_class = 'status-good' if frtx_mist <= frtx_m_soll else 'status-bad'
        
        clicked = st.button('', key='btn_frtx', help='📊 Cliquer pour voir le graphique détaillé', use_container_width=True, type='secondary')
        
        st.markdown(f"""
        <div class="metric-card {status_class}" style="margin-top: -60px; position: relative; z-index: 1; pointer-events: none;">
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
            <div style="position: absolute; top: 10px; right: 12px; font-size: 18px; opacity: 0.4;">📊</div>
        </div>
        """, unsafe_allow_html=True)
        
        if clicked:
            show_frtx_chart()
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # SECTION 2: LOGISTICS & PERFORMANCE
    st.markdown(f"<div class='section-header'>{t['logistics']}</div>", unsafe_allow_html=True)
    col5, col6, col7 = st.columns(3)
    
    with col5:
        color = 'green' if cycle_t_gap == 0 else 'red'
        status_class = 'status-good' if cycle_t_gap == 0 else 'status-bad'
        
        clicked = st.button('', key='btn_cycle', help='📊 Cliquer pour voir le graphique détaillé', use_container_width=True, type='secondary')
        
        st.markdown(f"""
        <div class="metric-card {status_class}" style="margin-top: -60px; position: relative; z-index: 1; pointer-events: none;">
            <div class="metric-header">{t['inventory']}</div>
            <div class="metric-value {color}">{cycle_tist:+.0f}€</div>
            <div class="metric-label">{t['variance']} ({t['limit']}: ±{cycle_grenze:.0f}€)</div>
            <div class="metric-sub">
                <div class="metric-sub-item">
                    <div class="metric-sub-value">{cycle_t_gap:+.0f}€</div>
                    <div class="metric-sub-label">{t['excess']}</div>
                </div>
            </div>
            <div style="position: absolute; top: 10px; right: 12px; font-size: 18px; opacity: 0.4;">📊</div>
        </div>
        """, unsafe_allow_html=True)
        
        if clicked:
            show_cycle_chart()
    
    with col6:
        color = 'green' if last_week['WCompleted'] >= last_week['WTotal'] else 'red'
        status_class = 'status-good' if last_week['WCompleted'] >= last_week['WTotal'] else 'status-bad'
        
        clicked = st.button('', key='btn_shipments', help='📊 Cliquer pour voir le graphique détaillé', use_container_width=True, type='secondary')
        
        st.markdown(f"""
        <div class="metric-card {status_class}" style="margin-top: -60px; position: relative; z-index: 1; pointer-events: none;">
            <div class="metric-header">{t['shipments']} ({t['week']} {last_week['Week']:.0f})</div>
            <div class="metric-value {color}">{last_week['WCompleted']:.0f}/{last_week['WTotal']:.0f}</div>
            <div class="metric-label">{t['deliveries_completed']}</div>
            <div class="metric-sub">
                <div class="metric-sub-item">
                    <div class="metric-sub-value">{w_gap:+.0f}</div>
                    <div class="metric-sub-label">{t['gap']}</div>
                </div>
            </div>
            <div style="position: absolute; top: 10px; right: 12px; font-size: 18px; opacity: 0.4;">📊</div>
        </div>
        """, unsafe_allow_html=True)
        
        if clicked:
            show_shipments_chart()
    
    with col7:
        color = 'green' if last_row['SAA_MIST'] >= saa_percent_soll else 'red'
        status_class = 'status-good' if last_row['SAA_MIST'] >= saa_percent_soll else 'status-bad'
        
        clicked = st.button('', key='btn_saa', help='📊 Cliquer pour voir le graphique détaillé', use_container_width=True, type='secondary')
        
        st.markdown(f"""
        <div class="metric-card {status_class}" style="margin-top: -60px; position: relative; z-index: 1; pointer-events: none;">
            <div class="metric-header">{t['saa']}</div>
            <div class="metric-value {color}">{last_row['SAA_MIST']:.0f}%</div>
            <div class="metric-label">{t['compliance']} ({t['target']}: {saa_percent_soll:.0f}%)</div>
            <div class="metric-sub">
                <div class="metric-sub-item">
                    <div class="metric-sub-value">{saa_m_gap:+.0f}%</div>
                    <div class="metric-sub-label">{t['vs_target']}</div>
                </div>
            </div>
            <div style="position: absolute; top: 10px; right: 12px; font-size: 18px; opacity: 0.4;">📊</div>
        </div>
        """, unsafe_allow_html=True)
        
        if clicked:
            show_saa_chart()
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # SECTION 3: ACTIONS & ABSENCES
    col8, col9 = st.columns([3, 1])
    
    with col8:
        # Espaceur pour aligner avec la carte Absences qui a un bouton invisible
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        
        st.markdown(f"<div class='section-header'>{t['actions']}</div>", unsafe_allow_html=True)
        
        # Préparer le DataFrame avec les bonnes colonnes
        actions_display = actions_df.copy()
        
        # Convertir les dates sans afficher les heures
        actions_display['Datum'] = pd.to_datetime(actions_display['Datum'], format='%Y-%m-%d', errors='coerce').dt.strftime('%d/%m/%Y')
        actions_display['Deadline'] = pd.to_datetime(actions_display['Deadline'], format='%Y-%m-%d', errors='coerce')
        actions_display['Deadline_display'] = actions_display['Deadline'].dt.strftime('%d/%m/%Y')
        
        # Sélectionner les colonnes à afficher (sans ID)
        actions_to_show = actions_display[['Thema', 'Datum', 'Verantwortlich', 'Aktion', 'Deadline_display', 'Status']].copy()
        
        # Renommer les colonnes selon la langue
        actions_to_show.columns = [
            t['col_theme'],
            t['col_date'],
            t['col_responsible'],
            t['col_action'],
            t['col_deadline'],
            t['col_status']
        ]
        
        # Fonction de coloration avec nouvelles règles
        def highlight_status(row):
            # Récupérer le statut et la deadline originale pour la comparaison
            idx = row.name
            status = actions_display.iloc[idx]['Status']
            deadline = actions_display.iloc[idx]['Deadline']
            
            # Vert si Completed
            if status == 'Completed':
                return ['background-color: #2e7d32; color: white; font-weight: bold'] * len(row)
            
            # Jaune si In progress ET deadline > date actuelle (encore du temps)
            elif status == 'In progress':
                if pd.notna(deadline) and deadline > current_date:
                    return ['background-color: #ffa726; color: white; font-weight: bold'] * len(row)
                else:
                    # En retard : rouge
                    return ['background-color: #c62828; color: white; font-weight: bold'] * len(row)
            
            # Rouge pour tous les autres cas (Not started, ou autres)
            else:
                return ['background-color: #c62828; color: white; font-weight: bold'] * len(row)
        
        st.dataframe(
            actions_to_show.style.apply(highlight_status, axis=1),
            use_container_width=True,
            hide_index=True,
            height=200
        )
    
    with col9:
        st.markdown(f"<div class='section-header'>{t['absences']}</div>", unsafe_allow_html=True)
        
        color = 'green' if last_row['Abwesenheit_TIST'] <= abw_t_soll else 'red'
        status_class = 'status-good' if last_row['Abwesenheit_TIST'] <= abw_t_soll else 'status-bad'
        
        clicked = st.button('', key='btn_abw', help='📊 Cliquer pour voir le graphique détaillé', use_container_width=True, type='secondary')
        
        st.markdown(f"""
        <div class="metric-card {status_class}" style="margin-top: -60px; position: relative; z-index: 1; pointer-events: none;">
            <div class="metric-value {color}" style="font-size: 56px;">{last_row['Abwesenheit_TIST']:.0f}</div>
            <div class="metric-label" style="font-size: 14px;">{t['absences_today']}</div>
            <div class="metric-sub" style="margin-top: 16px;">
                <div class="metric-sub-item">
                    <div class="metric-sub-value">{abw_t_gap:+.0f}</div>
                    <div class="metric-sub-label">{t['vs_target']} ({abw_t_soll:.0f})</div>
                </div>
            </div>
            <div style="position: absolute; top: 10px; right: 12px; font-size: 18px; opacity: 0.4;">📊</div>
        </div>
        """, unsafe_allow_html=True)
        
        if clicked:
            show_abw_chart()

# ============================================
# ONGLET 2: DETAILED ANALYTICS
# ============================================
with tab2:
    st.markdown(f"<h3 style='color: #1a237e; font-weight: 700; margin-bottom: 20px;'>{t['monthly_evolution']}</h3>", unsafe_allow_html=True)
    
    # Préparer les données cumulatives
    current_month_data = current_month_data.copy()
    current_month_data['Kunde_Cumul'] = current_month_data['Kunde_TIST'].cumsum()
    current_month_data['Liefer_Cumul'] = current_month_data['Liefer_TIST'].cumsum()
    current_month_data['FRTX_Cumul'] = current_month_data['FRTX_TIST'].cumsum()
    
    # Ajouter les 3 prochains jours ouvrés (si dans le même mois)
    last_date = current_month_data['Date'].max()
    
    # Calculer la fin du mois correctement
    if last_date.month == 12:
        month_end = last_date.replace(day=31)
    else:
        next_month = last_date.replace(day=28) + timedelta(days=4)
        month_end = next_month - timedelta(days=next_month.day)
    
    future_dates = []
    current_check = last_date + timedelta(days=1)
    
    while len(future_dates) < 3 and current_check <= month_end:
        # Vérifier si c'est un jour ouvré (lundi=0 à vendredi=4)
        if current_check.weekday() < 5:
            future_dates.append(current_check)
        current_check += timedelta(days=1)
    
    # Créer un DataFrame étendu avec les futures dates
    if future_dates:
        future_df = pd.DataFrame({
            'Date': future_dates,
            'Kunde_TIST': [None] * len(future_dates),
            'Liefer_TIST': [None] * len(future_dates),
            'RiskHunting_TIST': [None] * len(future_dates),
            'FRTX_TIST': [None] * len(future_dates),
            'CycleCounting_TIST': [None] * len(future_dates),
            'SAA_MIST': [None] * len(future_dates),
            'Abwesenheit_TIST': [None] * len(future_dates),
            'Kunde_Cumul': [None] * len(future_dates),
            'Liefer_Cumul': [None] * len(future_dates),
            'FRTX_Cumul': [None] * len(future_dates)
        })
        extended_data = pd.concat([current_month_data, future_df], ignore_index=True)
    else:
        extended_data = current_month_data
    
    # Créer l'objectif cumulatif qui croît jour par jour (y compris futures dates)
    days_so_far = list(range(1, len(current_month_data) + 1))
    kunde_cumul_soll = [kunde_t_soll * i for i in days_so_far]
    liefer_cumul_soll = [liefer_t_soll * i for i in days_so_far]
    
    # Étendre les objectifs pour les jours futurs
    if future_dates:
        for i in range(len(future_dates)):
            kunde_cumul_soll.append(kunde_t_soll * (len(current_month_data) + i + 1))
            liefer_cumul_soll.append(liefer_t_soll * (len(current_month_data) + i + 1))
    
    # SECTION 1: QUALITY & SAFETY
    st.markdown(f"<div class='section-header'>{t['quality_safety']}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Customer Complaints - BARRES CUMULATIVES
        fig_kunde = go.Figure()
        
        # Barres cumulatives avec couleurs conditionnelles (seulement pour les données réelles)
        bar_colors = ['#66bb6a' if val <= soll else '#ef5350' 
                      for val, soll in zip(current_month_data['Kunde_Cumul'], kunde_cumul_soll[:len(current_month_data)])]
        
        fig_kunde.add_trace(
            go.Bar(
                x=current_month_data['Date'],
                y=current_month_data['Kunde_Cumul'],
                name=t['cumulative'],
                marker_color=bar_colors,
                text=current_month_data['Kunde_Cumul'],
                textposition='outside',
                textfont=dict(color='#424242', size=10)
            )
        )
        
        # Ligne objectif cumulatif croissant (sur toutes les dates y compris futures)
        fig_kunde.add_trace(
            go.Scatter(
                x=extended_data['Date'],
                y=kunde_cumul_soll,
                name=t['objective'],
                line=dict(color='#b71c1c', width=3),  # Rouge foncé, trait plein
                mode='lines'
            )
        )
        
        fig_kunde.update_layout(
            title=dict(text=t['customer_complaints'], font=dict(color='#1a237e', size=14, family='Arial Black')),
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=350,
            margin=dict(l=10, r=10, t=60, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#424242')),
            font=dict(size=11, color='#424242')
        )
        
        fig_kunde.update_yaxes(
            title_text=t['cumulative'], 
            showgrid=True, 
            gridcolor='#f0f0f0', 
            title_font=dict(color='#424242'),
            rangemode='tozero'  # Forcer à partir de 0
        )
        fig_kunde.update_xaxes(
            showgrid=False, 
            tickfont=dict(color='#424242'),
            tickformat='%d/%m',
            dtick=86400000,  # Tous les jours
            range=[extended_data['Date'].min() - timedelta(hours=12), extended_data['Date'].max() + timedelta(hours=12)]
        )
        
        st.plotly_chart(fig_kunde, use_container_width=True)
    
    with col2:
        # Supplier Complaints - BARRES CUMULATIVES
        fig_liefer = go.Figure()
        
        # Barres cumulatives avec couleurs conditionnelles (seulement données réelles)
        bar_colors = ['#66bb6a' if val <= soll else '#ef5350' 
                      for val, soll in zip(current_month_data['Liefer_Cumul'], liefer_cumul_soll[:len(current_month_data)])]
        
        fig_liefer.add_trace(
            go.Bar(
                x=current_month_data['Date'],
                y=current_month_data['Liefer_Cumul'],
                name=t['cumulative'],
                marker_color=bar_colors,
                text=current_month_data['Liefer_Cumul'],
                textposition='outside',
                textfont=dict(color='#424242', size=10)
            )
        )
        
        # Ligne objectif cumulatif croissant (sur toutes les dates)
        fig_liefer.add_trace(
            go.Scatter(
                x=extended_data['Date'],
                y=liefer_cumul_soll,
                name=t['objective'],
                line=dict(color='#b71c1c', width=3),  # Rouge foncé, trait plein
                mode='lines'
            )
        )
        
        fig_liefer.update_layout(
            title=dict(text=t['supplier_complaints'], font=dict(color='#1a237e', size=14, family='Arial Black')),
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=350,
            margin=dict(l=10, r=10, t=60, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#424242')),
            font=dict(size=11, color='#424242')
        )
        
        fig_liefer.update_yaxes(
            title_text=t['cumulative'], 
            showgrid=True, 
            gridcolor='#f0f0f0', 
            title_font=dict(color='#424242'),
            rangemode='tozero'
        )
        fig_liefer.update_xaxes(
            showgrid=False, 
            tickfont=dict(color='#424242'),
            tickformat='%d/%m',
            dtick=86400000,
            range=[extended_data['Date'].min() - timedelta(hours=12), extended_data['Date'].max() + timedelta(hours=12)]
        )
        
        st.plotly_chart(fig_liefer, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        # Risk Hunting - Barres journalières vertes si >= objectif, rouges sinon
        fig_risk = go.Figure()
        
        bar_colors = ['#66bb6a' if val >= risk_t_soll else '#ef5350' for val in current_month_data['RiskHunting_TIST']]
        
        fig_risk.add_trace(
            go.Bar(
                x=current_month_data['Date'],
                y=current_month_data['RiskHunting_TIST'],
                name=t['daily_trend'],
                marker_color=bar_colors,
                text=current_month_data['RiskHunting_TIST'],
                textposition='outside',
                textfont=dict(color='#424242', size=10)
            )
        )
        
        fig_risk.add_trace(
            go.Scatter(
                x=extended_data['Date'],
                y=[risk_t_soll] * len(extended_data),
                name=t['objective'],
                line=dict(color='#b71c1c', width=3),
                mode='lines'
            )
        )
        
        fig_risk.update_layout(
            title=dict(text=t['risk_hunting'], font=dict(color='#1a237e', size=14, family='Arial Black')),
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=350,
            margin=dict(l=10, r=10, t=60, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#424242')),
            font=dict(size=11, color='#424242'),
            yaxis_title=t['risks_identified'],
            yaxis=dict(title_font=dict(color='#424242'), rangemode='tozero')
        )
        
        fig_risk.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
        fig_risk.update_xaxes(
            showgrid=False, 
            tickfont=dict(color='#424242'),
            tickformat='%d/%m',
            dtick=86400000,
            range=[extended_data['Date'].min() - timedelta(hours=12), extended_data['Date'].max() + timedelta(hours=12)]
        )
        
        st.plotly_chart(fig_risk, use_container_width=True)
    
    with col4:
        # FRTX - BARRES JOURNALIÈRES SEULEMENT (pas de cumul)
        fig_frtx = go.Figure()
        
        bar_colors = ['#66bb6a' if val == 0 else '#ef5350' for val in current_month_data['FRTX_TIST']]
        
        fig_frtx.add_trace(
            go.Bar(
                x=current_month_data['Date'],
                y=current_month_data['FRTX_TIST'],
                name=t['daily_trend'],
                marker_color=bar_colors,
                text=current_month_data['FRTX_TIST'],
                textposition='outside',
                textfont=dict(color='#424242', size=10)
            )
        )
        
        # Ligne objectif journalier (sur toutes les dates)
        fig_frtx.add_trace(
            go.Scatter(
                x=extended_data['Date'],
                y=[frtx_t_soll] * len(extended_data),
                name=t['objective'],
                line=dict(color='#b71c1c', width=3),
                mode='lines'
            )
        )
        
        fig_frtx.update_layout(
            title=dict(text=t['frtx'], font=dict(color='#1a237e', size=14, family='Arial Black')),
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=350,
            margin=dict(l=10, r=10, t=60, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#424242')),
            font=dict(size=11, color='#424242')
        )
        
        fig_frtx.update_yaxes(title_text=t['daily_trend'], showgrid=True, gridcolor='#f0f0f0', title_font=dict(color='#424242'), rangemode='tozero')
        fig_frtx.update_xaxes(
            showgrid=False, 
            tickfont=dict(color='#424242'),
            tickformat='%d/%m',
            dtick=86400000,
            range=[extended_data['Date'].min() - timedelta(hours=12), extended_data['Date'].max() + timedelta(hours=12)]
        )
        
        st.plotly_chart(fig_frtx, use_container_width=True)
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # SECTION 2: LOGISTICS & PERFORMANCE
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
                marker=dict(size=6),
                fill='tonexty',
                fillcolor='rgba(198, 40, 40, 0.1)'
            )
        )
        
        # Zone de tolérance (sur toutes les dates)
        fig_cycle.add_trace(
            go.Scatter(
                x=extended_data['Date'],
                y=[cycle_grenze] * len(extended_data),
                name=f'+{cycle_grenze:.0f}€',
                line=dict(color='#ffa726', width=1, dash='dot'),
                mode='lines'
            )
        )
        
        fig_cycle.add_trace(
            go.Scatter(
                x=extended_data['Date'],
                y=[-cycle_grenze] * len(extended_data),
                name=f'-{cycle_grenze:.0f}€',
                line=dict(color='#ffa726', width=1, dash='dot'),
                mode='lines',
                fill='tonexty',
                fillcolor='rgba(102, 187, 106, 0.1)'
            )
        )
        
        fig_cycle.update_layout(
            title=dict(text=t['inventory'], font=dict(color='#1a237e', size=14, family='Arial Black')),
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=350,
            margin=dict(l=10, r=10, t=60, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#424242')),
            font=dict(size=11, color='#424242'),
            yaxis_title='€',
            yaxis=dict(title_font=dict(color='#424242'))
        )
        
        fig_cycle.update_yaxes(showgrid=True, gridcolor='#f0f0f0', zeroline=True, zerolinecolor='#666')
        fig_cycle.update_xaxes(
            showgrid=False, 
            tickfont=dict(color='#424242'),
            tickformat='%d/%m',
            dtick=86400000,
            range=[extended_data['Date'].min() - timedelta(hours=12), extended_data['Date'].max() + timedelta(hours=12)]
        )
        
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
                marker=dict(size=6),
                fill='tozeroy',
                fillcolor='rgba(46, 125, 50, 0.1)'
            )
        )
        
        fig_saa.add_trace(
            go.Scatter(
                x=extended_data['Date'],
                y=[saa_percent_soll] * len(extended_data),
                name=t['objective'],
                line=dict(color='#b71c1c', width=3),
                mode='lines'
            )
        )
        
        fig_saa.update_layout(
            title=dict(text=t['saa'], font=dict(color='#1a237e', size=14, family='Arial Black')),
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=350,
            margin=dict(l=10, r=10, t=60, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#424242')),
            font=dict(size=11, color='#424242'),
            yaxis_title='%',
            yaxis=dict(range=[80, 100], title_font=dict(color='#424242'))
        )
        
        fig_saa.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
        fig_saa.update_xaxes(
            showgrid=False, 
            tickfont=dict(color='#424242'),
            tickformat='%d/%m',
            dtick=86400000,
            range=[extended_data['Date'].min() - timedelta(hours=12), extended_data['Date'].max() + timedelta(hours=12)]
        )
        
        st.plotly_chart(fig_saa, use_container_width=True)
    
    with col7:
        # Absences - Barres vertes si <= objectif, rouges sinon
        fig_abw = go.Figure()
        
        bar_colors = ['#ef5350' if x > abw_t_soll else '#66bb6a' for x in current_month_data['Abwesenheit_TIST']]
        
        fig_abw.add_trace(
            go.Bar(
                x=current_month_data['Date'],
                y=current_month_data['Abwesenheit_TIST'],
                name=t['absences_today'],
                marker_color=bar_colors,
                text=current_month_data['Abwesenheit_TIST'],
                textposition='outside',
                textfont=dict(color='#424242', size=10)
            )
        )
        
        fig_abw.add_trace(
            go.Scatter(
                x=extended_data['Date'],
                y=[abw_t_soll] * len(extended_data),
                name=t['objective'],
                line=dict(color='#b71c1c', width=3),
                mode='lines'
            )
        )
        
        fig_abw.update_layout(
            title=dict(text=t['absences'], font=dict(color='#1a237e', size=14, family='Arial Black')),
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=350,
            margin=dict(l=10, r=10, t=60, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#424242')),
            font=dict(size=11, color='#424242'),
            yaxis_title=t['absences_today'],
            yaxis=dict(title_font=dict(color='#424242'), rangemode='tozero')
        )
        
        fig_abw.update_yaxes(showgrid=True, gridcolor='#f0f0f0')
        fig_abw.update_xaxes(
            showgrid=False, 
            tickfont=dict(color='#424242'),
            tickformat='%d/%m',
            dtick=86400000,
            range=[extended_data['Date'].min() - timedelta(hours=12), extended_data['Date'].max() + timedelta(hours=12)]
        )
        
        st.plotly_chart(fig_abw, use_container_width=True)
    
    # Ligne 4: Shipments (graphique hebdomadaire)
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    col_ship = st.columns(1)[0]
    
    with col_ship:
        # Shipments - Graphique hebdomadaire avec barres groupées
        fig_ship_analytics = go.Figure()
        
        # Extraire les 5 dernières semaines
        recent_weeks = weekly_df.tail(5) if len(weekly_df) >= 5 else weekly_df
        
        # Positions des barres
        weeks = recent_weeks['Week'].astype(str)
        x_positions = list(range(len(weeks)))
        bar_width = 0.35
        
        # Barres réalisées (à gauche)
        completed = recent_weeks['WCompleted'].values
        total = recent_weeks['WTotal'].values
        bar_colors_completed = ['#66bb6a' if c >= t else '#ef5350' for c, t in zip(completed, total)]
        
        fig_ship_analytics.add_trace(
            go.Bar(
                x=[i - bar_width/2 for i in x_positions],
                y=completed,
                name=t['actual'],
                marker_color=bar_colors_completed,
                width=bar_width,
                text=completed,
                textposition='outside',
                textfont=dict(color='#424242', size=10)
            )
        )
        
        # Barres total attendu (à droite, bleu foncé)
        fig_ship_analytics.add_trace(
            go.Bar(
                x=[i + bar_width/2 for i in x_positions],
                y=total,
                name='Total',
                marker_color='#1565c0',
                width=bar_width,
                text=total,
                textposition='outside',
                textfont=dict(color='#424242', size=10)
            )
        )
        
        fig_ship_analytics.update_layout(
            title=dict(text=t['shipments'], font=dict(color='#1a237e', size=14, family='Arial Black')),
            xaxis=dict(
                tickmode='array',
                tickvals=x_positions,
                ticktext=[f"{t['week']} {w}" for w in weeks],
                title='',
                tickfont=dict(color='#424242')
            ),
            yaxis=dict(
                title=t['deliveries_completed'],
                title_font=dict(color='#424242'),
                showgrid=True,
                gridcolor='#f0f0f0',
                rangemode='tozero'
            ),
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=350,
            margin=dict(l=10, r=10, t=60, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(color='#424242')),
            font=dict(size=11, color='#424242'),
            barmode='group'
        )
        
        st.plotly_chart(fig_ship_analytics, use_container_width=True)