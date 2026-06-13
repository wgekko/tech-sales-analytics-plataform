import streamlit as st
import plotly.express as px
import pandas as pd

from utils import load_data

df = load_data()

st.set_page_config(page_title="Quant Options Analytics", layout="wide", page_icon=":material/analytics:")

st.subheader("Dashboard Ejecutivo")

ventas = df["total"].sum()
utilidad = df["utilidad"].sum()
ticket = df["total"].mean()
cantidad = df["cantidad"].sum()

c1,c2,c3,c4 = st.columns(4)

c1.metric("Ventas",f"${ventas:,.0f}")
c2.metric("Utilidad",f"${utilidad:,.0f}")
c3.metric("Ticket",f"${ticket:,.0f}")
c4.metric("Cantidad",f"{cantidad:,.0f}")

top = (
    df.groupby("producto")
    ["total"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig = px.bar(
    top,
    orientation="h",
    title="Top Productos"
)

st.plotly_chart(fig,width='stretch')

fig = px.treemap(
    df,
    path=[
        "categoria",
        "producto"
    ],
    values="total",
    color="utilidad"
)

st.plotly_chart(
    fig,
    width='stretch'
)

fig = px.sunburst(
    df,
    path=[
        "pais",
        "categoria",
        "producto"
    ],
    values="total"
)

tabla = pd.pivot_table(
    df,
    values="total",
    index="pais",
    columns="mes",
    aggfunc="sum"
)

import plotly.figure_factory as ff

fig = ff.create_annotated_heatmap(
    z=tabla.values,
    x=list(tabla.columns),
    y=list(tabla.index)
)


fig = px.sunburst(
    df,
    path=[
        "pais",
        "categoria",
        "producto"
    ],
    values="total"
)

st.plotly_chart(
    fig,
    width='stretch'
)

