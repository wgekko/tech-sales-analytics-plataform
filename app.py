# import streamlit as st

# st.set_page_config(
#     page_title="Tech Sales Analytics",
#     page_icon="📊",
#     layout="wide"
# )

# st.title("📊 Tech Sales Analytics Platform")

# st.markdown("""
# ### Funcionalidades

# - Dashboard Ejecutivo
# - Geografía Comercial
# - K-Means Clustering
# - Detección de Anomalías
# - Forecasting
# - Insights Automáticos

# Seleccione una página desde el menú lateral.
# """)


# 

import streamlit as st

st.set_page_config(
    page_title="Tech Sales Analytics Platform",
    page_icon=":material/sdk:",
    layout="wide"
)

st.subheader(":material/sdk: Tech Sales Analytics Platform")

st.markdown("""
## Plataforma de Inteligencia Comercial, Machine Learning y Forecasting

Solución integral para análisis de ventas, rentabilidad, inventario,
segmentación, predicción y monitoreo ejecutivo de una tienda tecnológica.
""")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:

    st.subheader(":material/checkbook: Business Intelligence")

    st.markdown("""
    - Dashboard Ejecutivo
    - Geografía Comercial
    - Business Health
    - Command Center
    - Executive Report
    """)

with col2:

    st.subheader(":material/dashboard_2_gear: Machine Learning")

    st.markdown("""
    - K-Means Clustering
    - Detección de Anomalías
    - Ranking Intelligence
    - Predictive Models
    """)

with col3:

    st.subheader(":material/smart_toy: Forecast & AI")

    st.markdown("""
    - Forecast Center
    - AI Insights
    - What-If Simulator
    - Seasonality Analysis
    """)

st.divider()

st.subheader(":material/add_location_alt: Mapa de Navegación")

st.markdown("""

### Business Intelligence

- Dashboard Ejecutivo
- Geografía Comercial
- Business Health
- Command Center
- Executive Report

### Machine Learning

- K-Means Clustering
- Detección de Anomalías
- Ranking Intelligence
- Predictive Models

### Forecasting & AI

- Forecast Center
- AI Insights
- What-If Simulator
- Seasonality Analysis

### Product Analytics

- Product Intelligence
    - Portfolio Analysis
    - ABC Analysis
    - Inventory Optimization
    - Margin Analysis
    - Product Lifetime Value

""")

st.divider()

st.subheader(":material/sweep: Objetivos de la Plataforma")

st.info("""
✔ Monitorear ventas y utilidad

✔ Detectar oportunidades comerciales

✔ Segmentar productos automáticamente

✔ Detectar anomalías de negocio

✔ Optimizar inventario

✔ Mejorar rentabilidad

✔ Generar forecasts de ventas

✔ Simular escenarios futuros

✔ Obtener recomendaciones automáticas

✔ Medir la salud general del negocio
""")

st.divider()

st.subheader(":material/list_alt: Arquitectura Actual")

st.code("""
app.py

pages/
│
├── 01_Dashboard.py
│        
├── 02_Geografia.py
│
├── 03_KMeans.py
│        
├── 04_Anomalias.py
│
├── 05_Forecast_Center.py
│        
├── 06_AI_Insights.py
│
├── 07_RFM.py
│        
├── 08_Ranking_Intelligence.py
│        
├── 09_Predictive_Models.py
│
├── 10_What_If_Simulator.py
│
├── 11_Business_Health.py
│
├── 12_Product_Intelligence.py
│
├── 13_Command_Center.py
│
├── 14_Seasonality_Analysis.py
│
├── 15_Executive_Report.py
│
└── data/
    └── db-datos.xlsx

models/
│
├── forecast.py
├── anomalies.py
├── backtesting.py
├── llm-insights.py                
├── kmeans.py
└── predictive.py
└── ranking.py 
└── rfm.py               

utils.py
        
utils_pdf.py        

""")

st.divider()

st.subheader(":material/receipt: Estado de Madurez Analítica")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "BI",
    "100%"
)

c2.metric(
    "Machine Learning",
    "90%"
)

c3.metric(
    "Forecasting",
    "95%"
)

c4.metric(
    "Automatización",
    "85%"
)

st.success(
    """
Plataforma consolidada en módulos de negocio.

Menos páginas, menos mantenimiento y una experiencia de navegación más profesional.
"""
)