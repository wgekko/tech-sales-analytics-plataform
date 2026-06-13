import pandas as pd
import streamlit as st

@st.cache_data
def load_data():

    df = pd.read_excel("data/db-datos.xlsx")

    df.columns = df.columns.str.lower()

    if "fecha" in df.columns:
        df["fecha"] = pd.to_datetime(df["fecha"])

    return df

