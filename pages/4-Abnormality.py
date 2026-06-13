import streamlit as st

from utils import load_data
from models.anomalies import detect_anomalies

st.set_page_config(page_title="K-Means", layout="wide", page_icon=":material/fork_left:")

df = load_data()

st.subheader(":material/fork_left: Detección de Anomalías")

df = detect_anomalies(df)

anomalias = df[df["anomalia"] == -1]

st.metric(
    "Anomalías Detectadas",
    len(anomalias)
)

st.dataframe(anomalias)


import plotly.express as px

fig = px.scatter(
    df,
    x="total",
    y="utilidad",
    color="anomalia"
)

st.plotly_chart(
    fig,
    width='stretch'
)