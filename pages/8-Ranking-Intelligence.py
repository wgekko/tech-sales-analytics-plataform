import streamlit as st

from utils import load_data
from models.ranking import ranking_productos

st.set_page_config(
    page_title="Ranking-Intelligence",
    page_icon=":material/leaderboard:",
    layout="wide"
)

df = load_data()

st.subheader(":material/leaderboard: Ranking Inteligente")

ranking = ranking_productos(df)

st.dataframe(ranking)

st.bar_chart(
    ranking["score"].head(20)
)

def categoria(score):

    if score >= 0.80:
        return ":material/trophy: Oro"

    elif score >= 0.50:
        return ":material/trophy: Plata"

    else:
        return ":material/trophy: Bronce"

ranking["nivel"] = ranking["score"].apply(categoria)