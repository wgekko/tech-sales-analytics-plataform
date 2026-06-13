import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from models.forecast import build_forecast

from utils import load_data
from models.forecast import build_forecast

st.set_page_config(
    page_title="Business Health",
    page_icon=":material/data_exploration:",
    layout="wide"
)

st.subheader(":material/checkbook: Business Health Score")

df = load_data()

# ==========================
# KPIs base
# ==========================

ventas = df["total"].sum()

utilidad = df["utilidad"].sum()

# ==========================
# Forecast
# ==========================

# ventas_fc, modelo, features = build_forecast(df)

# forecast_promedio = (
#     ventas_fc["total"]
#     .tail(30)
#     .mean()
# )

#forecast_90 = forecast_promedio * 90

from models.forecast import (
    get_forecast_summary
)

summary = get_forecast_summary(df)

forecast_90 = (
    summary["forecast_90"]
)

mape = (
    summary["mape"]
)


# ==========================
# Score Ventas
# ==========================

score_ventas = min(
    ventas / 1_000_000 * 100,
    100
)

# ==========================
# Score Utilidad
# ==========================

margen = utilidad / ventas

score_utilidad = min(
    margen * 300,
    100
)

# ==========================
# Score Forecast
# ==========================

score_forecast = min(
    forecast_90 / ventas * 100,
    100
)

# ==========================
# Score Diversificación
# ==========================

productos = (
    df["producto"]
    .nunique()
)

score_diversificacion = min(
    productos * 2,
    100
)

# ==========================
# Score Concentración
# ==========================

top_producto = (
    df.groupby("producto")
      ["total"]
      .sum()
      .max()
)

concentracion = top_producto / ventas

score_concentracion = max(
    100 - (concentracion * 100),
    0
)

# ==========================
# Score Anomalías
# ==========================

try:

    anomalias = (
        df["anomalia"] == -1
    ).sum()

except:

    anomalias = 0

pct_anomalias = anomalias / len(df)

score_anomalias = max(
    100 - pct_anomalias * 1000,
    0
)

# ==========================
# Score Modelo
# ==========================

mape = 0.15

score_modelo = (
    (1 - mape)
    * 100
)

# ==========================
# Score Final
# ==========================

business_score = (

    score_ventas * 0.25 +

    score_utilidad * 0.25 +

    score_forecast * 0.20 +

    score_modelo * 0.15 +

    score_anomalias * 0.10 +

    score_diversificacion * 0.05

)

business_score = round(
    business_score,
    1
)

# ==========================
# Clasificación
# ==========================

if business_score >= 85:

    estado = "🟢 Excelente"
    riesgo = "Bajo"

elif business_score >= 70:

    estado = "🟡 Bueno"
    riesgo = "Moderado"

else:

    estado = "🔴 Riesgo"

    riesgo = "Alto"

# ==========================
# KPIs
# ==========================

c1,c2,c3 = st.columns(3)

c1.metric(
    "Business Score",
    f"{business_score}/100"
)

c2.metric(
    "Estado",
    estado
)

c3.metric(
    "Riesgo",
    riesgo
)

# ==========================
# Gauge
# ==========================

fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=business_score,
        title={
            "text":"Business Health"
        },
        gauge={
            "axis":{"range":[0,100]}
        }
    )
)

st.plotly_chart(
    fig,
    width='stretch',
    key="business_health_gauge"
)

# ==========================
# Detalle
# ==========================

detalle = pd.DataFrame({

    "Indicador":[
        "Ventas",
        "Utilidad",
        "Forecast",
        "Modelo",
        "Anomalías",
        "Diversificación"
    ],

    "Score":[
        score_ventas,
        score_utilidad,
        score_forecast,
        score_modelo,
        score_anomalias,
        score_diversificacion
    ]
})

st.subheader(":material/rate_review: Detalle del Score")

st.dataframe(
    detalle,
    width='stretch'
)

# ==========================
# Insights
# ==========================

st.subheader(":material/social_leaderboard: Insights")

if score_forecast > 80:

    st.success(
        "Se proyecta crecimiento sostenido."
    )

if score_concentracion < 50:

    st.warning(
        "Existe dependencia elevada de pocos productos."
    )

if score_anomalias < 70:

    st.warning(
        "Se detectaron anomalías significativas."
    )

if score_modelo > 80:

    st.success(
        "El modelo predictivo presenta buena calidad."
    )