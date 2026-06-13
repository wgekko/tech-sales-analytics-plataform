import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_data

st.set_page_config(
    page_title="Product Intelligence",
    page_icon=":material/inventory:",
    layout="wide"
)

st.subheader(":material/inventory: Product Intelligence Center")

df = load_data()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    " :material/menu: Portfolio",
    " :material/menu: ABC",
    " :material/menu: Inventario",
    " :material/menu: Margen",
    " :material/menu: Lifetime Value"
])

with tab1:

    st.subheader("Portfolio Optimization")

    portfolio = (
        df.groupby("producto")
        .agg({
            "total":"sum",
            "utilidad":"sum",
            "cantidad":"sum"
        })
        .reset_index()
    )

    portfolio["crecimiento"] = (
        portfolio["total"]
        .pct_change()
        .fillna(0)
    )

    med_ventas = portfolio["total"].median()
    med_crecimiento = portfolio["crecimiento"].median()

    def clasificar(row):

        if (
            row["total"] >= med_ventas and
            row["crecimiento"] >= med_crecimiento
        ):
            return "Estratégico"

        elif row["utilidad"] >= portfolio["utilidad"].median():
            return "Rentable"

        elif row["crecimiento"] >= med_crecimiento:
            return "Crecimiento"

        else:
            return "Optimización"

    portfolio["segmento"] = (
        portfolio.apply(
            clasificar,
            axis=1
        )
    )

    fig = px.scatter(
        portfolio,
        x="utilidad",
        y="total",
        size="cantidad",
        color="segmento",
        hover_name="producto"
    )

    st.plotly_chart(
        fig,
        width='stretch',
        key="portfolio_scatter"
    )

with tab2:

    st.subheader("ABC Analysis")

    abc = (
        df.groupby("producto")
        ["total"]
        .sum()
        .sort_values(
            ascending=False
        )
        .reset_index()
    )

    abc["acumulado"] = (
        abc["total"]
        .cumsum()
        /
        abc["total"].sum()
    ) * 100

    def categoria_abc(x):

        if x <= 80:
            return "A"

        elif x <= 95:
            return "B"

        return "C"

    abc["ABC"] = (
        abc["acumulado"]
        .apply(categoria_abc)
    )

    st.dataframe(
        abc,
        width='stretch'
    )

    fig = px.histogram(
        abc,
        x="ABC"
    )

    st.plotly_chart(
        fig,
        width='stretch',
        key="abc_chart"
    )

with tab3:

    st.subheader("Inventory Optimization")

    inv = (
        df.groupby("producto")
        .agg({
            "cantidad":"sum",
            "utilidad":"sum",
            "total":"sum"
        })
        .reset_index()
    )

    inv["rotacion"] = (
        inv["cantidad"]
        /
        inv["cantidad"].mean()
    )

    fig = px.scatter(
        inv,
        x="cantidad",
        y="total",
        size="utilidad",
        hover_name="producto",
        color="rotacion"
    )

    st.plotly_chart(
        fig,
        width='stretch',
        key="inventory_chart"
    )

    alta = inv[
        inv["rotacion"] > 1.5
    ]

    baja = inv[
        inv["rotacion"] < 0.5
    ]

    c1,c2 = st.columns(2)

    c1.metric(
        "Alta Rotación",
        len(alta)
    )

    c2.metric(
        "Baja Rotación",
        len(baja)
    )

with tab4:

    st.subheader("Margin Analysis")

    margen = (
        df.groupby("producto")
        .agg({
            "total":"sum",
            "utilidad":"sum"
        })
        .reset_index()
    )

    margen["margen"] = (
        margen["utilidad"]
        /
        margen["total"]
    ) * 100

    fig = px.bar(
        margen.sort_values(
            "margen",
            ascending=False
        ).head(20),
        x="producto",
        y="margen"
    )

    st.plotly_chart(
        fig,
        width='stretch',
        key="margin_chart"
    )

    st.dataframe(
        margen.sort_values(
            "margen",
            ascending=False
        ),
        width='stretch'
    )            

with tab5:

    st.subheader(
        "Product Lifetime Value"
    )

    plv = (
        df.groupby("producto")
        .agg({
            "total":"sum",
            "utilidad":"sum",
            "cantidad":"sum"
        })
        .reset_index()
    )

    plv["plv"] = (
        plv["utilidad"]
        *
        plv["cantidad"]
    )

    fig = px.bar(
        plv.sort_values(
            "plv",
            ascending=False
        ).head(15),
        x="producto",
        y="plv"
    )

    st.plotly_chart(
        fig,
        width='stretch',
        key="plv_chart"
    )

    st.dataframe(
        plv.sort_values(
            "plv",
            ascending=False
        ),
        width='stretch'
    )







