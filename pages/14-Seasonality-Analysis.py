import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

from utils import load_data

st.set_page_config(
    page_title="Seasonality Analysis",
    page_icon=":material/add_chart:",
    layout="wide"
)

st.title(":material/add_chart: Seasonality Analysis")

df = load_data()

df["fecha"] = pd.to_datetime(df["fecha"])

# ==========================
# Mes y Día Semana
# ==========================

meses = {
    1:"Enero",
    2:"Febrero",
    3:"Marzo",
    4:"Abril",
    5:"Mayo",
    6:"Junio",
    7:"Julio",
    8:"Agosto",
    9:"Septiembre",
    10:"Octubre",
    11:"Noviembre",
    12:"Diciembre"
}

dias = {
    0:"Lunes",
    1:"Martes",
    2:"Miércoles",
    3:"Jueves",
    4:"Viernes",
    5:"Sábado",
    6:"Domingo"
}

df["mes_nombre"] = df["fecha"].dt.month.map(meses)
df["dia_semana"] = df["fecha"].dt.dayofweek.map(dias)

# ==========================
# Ventas por Mes
# ==========================

st.subheader(":material/frame_inspect: Ventas por Mes")

ventas_mes = (
    df.groupby("mes_nombre")["total"]
      .sum()
      .reset_index()
)

orden_meses = list(meses.values())

ventas_mes["mes_nombre"] = pd.Categorical(
    ventas_mes["mes_nombre"],
    categories=orden_meses,
    ordered=True
)

ventas_mes = ventas_mes.sort_values(
    "mes_nombre"
)

fig_mes = px.bar(
    ventas_mes,
    x="mes_nombre",
    y="total",
    title="Ventas por Mes"
)

st.plotly_chart(
    fig_mes,
    width='stretch',
    key="ventas_mes"
)

# ==========================
# Ventas por Día Semana
# ==========================

st.subheader(":material/monitor_weight_loss: Ventas por Día de Semana")

ventas_dia = (
    df.groupby("dia_semana")["total"]
      .sum()
      .reset_index()
)

orden_dias = list(dias.values())

ventas_dia["dia_semana"] = pd.Categorical(
    ventas_dia["dia_semana"],
    categories=orden_dias,
    ordered=True
)

ventas_dia = ventas_dia.sort_values(
    "dia_semana"
)

fig_dia = px.bar(
    ventas_dia,
    x="dia_semana",
    y="total",
    title="Ventas por Día"
)

st.plotly_chart(
    fig_dia,
    width='stretch',
    key="ventas_dia"
)

# ==========================
# Heatmap Mes x Día
# ==========================

st.subheader(":material/data_table: Heatmap Estacional")

heat = pd.pivot_table(
    df,
    values="total",
    index=df["fecha"].dt.month,
    columns=df["fecha"].dt.dayofweek,
    aggfunc="sum",
    fill_value=0
)

fig_heat = ff.create_annotated_heatmap(
    z=heat.values,
    x=[
        "Lun","Mar","Mié",
        "Jue","Vie","Sáb","Dom"
    ],
    y=[
        "Ene","Feb","Mar","Abr",
        "May","Jun","Jul","Ago",
        "Sep","Oct","Nov","Dic"
    ][:len(heat.index)]
)

st.plotly_chart(
    fig_heat,
    width='stretch',
    key="heatmap_estacional"
)

# ==========================
# Mejores Meses
# ==========================

st.subheader(":material/table_chart_view: Mejores Meses")

top_meses = (
    df.groupby(df["fecha"].dt.month)["total"]
      .sum()
      .sort_values(ascending=False)
      .head(3)
)

st.dataframe(
    top_meses,
    width='stretch'
)

# ==========================
# Peores Meses
# ==========================

st.subheader(":material/warning: Meses Débiles")

peores_meses = (
    df.groupby(df["fecha"].dt.month)["total"]
      .sum()
      .sort_values()
      .head(3)
)

st.dataframe(
    peores_meses,
    width='stretch'
)

# ==========================
# Insight automático
# ==========================

mejor_mes = top_meses.index[0]
peor_mes = peores_meses.index[0]

st.success(
    f"""
:material/download_done: Mejor mes: {meses[mejor_mes]}

:material/file_download_off: Mes más débil: {meses[peor_mes]}

:material/data_object: Utilice esta información para ajustar campañas,
stock y forecast.
"""
)