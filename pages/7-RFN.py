import streamlit as st
import plotly.express as px

from utils import load_data
from models.rfm import build_rfm

st.set_page_config(
    page_title="RFN",
    page_icon=":material/barcode_scanner:",
    layout="wide"
)

df = load_data()

st.title(":material/barcode_scanner: RFM Productos")

rfm = build_rfm(df)

fig = px.scatter(
    rfm,
    x="Frequency",
    y="Monetary",
    size="Monetary",
    hover_name=rfm.index
)

st.plotly_chart(fig,width='stretch')

st.dataframe(rfm)