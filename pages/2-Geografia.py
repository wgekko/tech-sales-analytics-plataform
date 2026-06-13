import streamlit as st
import plotly.express as px

from utils import load_data

st.set_page_config(page_title="Geography", layout="wide", page_icon=":material/globe_location_pin:")


df = load_data()

st.subheader(":material/globe_location_pin: Geografía Comercial")

paises = (
    df.groupby("pais")
    ["total"]
    .sum()
    .reset_index()
)

fig = px.choropleth(
    paises,
    locations="pais",
    locationmode="country names",
    color="total"
)

st.plotly_chart(fig,width='stretch')

ciudades = (
    df.groupby("ciudad")
    ["total"]
    .sum()
    .sort_values(ascending=False)
    .head(20)
)

st.bar_chart(ciudades)