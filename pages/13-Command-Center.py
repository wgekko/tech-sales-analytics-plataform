import streamlit as st
import plotly.express as px
import pandas as pd

from utils import load_data

st.set_page_config(
    page_title="Command Center",
    layout="wide",
    page_icon=":material/chat_paste_go:"
)

st.subheader(":material/chat_paste_go: Command Center")

df = load_data()

# ==========================
# KPIs principales
# ==========================

ventas = df["total"].sum()

utilidad = df["utilidad"].sum()

productos = df["producto"].nunique()

ciudades = df["ciudad"].nunique()

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Ventas",
    f"${ventas:,.0f}"
)

c2.metric(
    "Utilidad",
    f"${utilidad:,.0f}"
)

c3.metric(
    "Productos",
    productos
)

c4.metric(
    "Ciudades",
    ciudades
)

# ==========================
# Segunda fila KPIs
# ==========================

margen = utilidad / ventas

ticket = df["total"].mean()

cantidad = df["cantidad"].sum()

paises = df["pais"].nunique()

c5,c6,c7,c8 = st.columns(4)

c5.metric(
    "Margen",
    f"{margen:.1%}"
)

c6.metric(
    "Ticket Promedio",
    f"${ticket:,.0f}"
)

c7.metric(
    "Unidades",
    f"{cantidad:,.0f}"
)

c8.metric(
    "Países",
    paises
)

# ==========================
# Producto líder
# ==========================

producto_top = (
    df.groupby("producto")
      ["total"]
      .sum()
      .idxmax()
)

ventas_top = (
    df.groupby("producto")
      ["total"]
      .sum()
      .max()
)

st.success(
    f":material/social_leaderboard: Producto líder: {producto_top} | Ventas: ${ventas_top:,.0f}"
)

# ==========================
# Treemap
# ==========================

st.subheader(":material/inbox_text: Productos por Categoría")

fig_treemap = px.treemap(
    df,
    path=[
        "categoria",
        "producto"
    ],
    values="total",
    color="utilidad"
)

st.plotly_chart(
    fig_treemap,
    width='stretch',
    key="command_treemap"
)

# ==========================
# Sunburst Geográfico
# ==========================

st.subheader(":material/globe_location_pin: Distribución Geográfica")

fig_sunburst = px.sunburst(
    df,
    path=[
        "pais",
        "ciudad",
        "categoria",
        "producto"
    ],
    values="total"
)

st.plotly_chart(
    fig_sunburst,
    width='stretch',
    key="command_sunburst"
)

# ==========================
# Top 10 Productos
# ==========================

st.subheader(":material/subheader: Top 10 Productos")

top_productos = (
    df.groupby("producto")
      ["total"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

fig_top = px.bar(
    top_productos,
    x="producto",
    y="total",
    title="Top Productos"
)

st.plotly_chart(
    fig_top,
    width='stretch',
    key="command_top_productos"
)

# ==========================
# Top Ciudades
# ==========================

st.subheader(":material/top_panel_close: Top Ciudades")

top_ciudades = (
    df.groupby("ciudad")
      ["total"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .reset_index()
)

fig_ciudad = px.bar(
    top_ciudades,
    x="ciudad",
    y="total",
    title="Top Ciudades"
)

st.plotly_chart(
    fig_ciudad,
    width='stretch',
    key="command_top_ciudades"
)

# ==========================
# Resumen Ejecutivo
# ==========================

st.subheader(":material/share_reviews: Resumen Ejecutivo")

categoria_top = (
    df.groupby("categoria")
      ["total"]
      .sum()
      .idxmax()
)

pais_top = (
    df.groupby("pais")
      ["total"]
      .sum()
      .idxmax()
)

st.info(
    f"""
:material/data_info_alert: Producto líder: {producto_top}

:material/data_info_alert: Categoría líder: {categoria_top}

:material/data_info_alert: País líder: {pais_top}

:material/data_info_alert: Margen global: {margen:.1%}

:material/data_info_alert: Ventas totales: ${ventas:,.0f}

:material/data_info_alert: Utilidad total: ${utilidad:,.0f}
"""
)

# ==========================
# Estado Plataforma
# ==========================

st.subheader(":material/analytics: Estado Analítico")

st.success(
    """
✅ Dashboard operativo

✅ Forecast operativo

✅ KMeans operativo

✅ Detección de anomalías operativa

✅ Business Health operativo

✅ Portfolio Optimization operativo

✅ Product Lifetime Value operativo

✅ ABC Analysis operativo
"""
)