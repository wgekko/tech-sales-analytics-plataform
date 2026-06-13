import streamlit as st
import plotly.express as px

from utils import load_data
from models.kmeans import run_kmeans

st.set_page_config(page_title="K-Means", layout="wide", page_icon=":material/robot_2:")

df = load_data()

st.title(":material/robot_2: K-Means Clustering")

opcion = st.selectbox(
    "Segmentar",
    [
        "producto",
        "ciudad",
        "pais"
    ]
)

resultado = run_kmeans(df, opcion)

fig = px.scatter(
    resultado,
    x="x",
    y="y",
    color="cluster",
    hover_name=resultado.index
)

st.plotly_chart(
    fig,
    width='stretch'
)

st.dataframe(resultado)

