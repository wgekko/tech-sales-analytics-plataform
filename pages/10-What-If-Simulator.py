import streamlit as st
import plotly.graph_objects as go

from utils import load_data

st.set_page_config(
    page_title="What-If-Simulator",
    page_icon=":material/schema:",
    layout="wide"
)


st.subheader(":material/schema: What If Simulator")

df = load_data()

ventas_actuales = df["total"].sum()

utilidad_actual = df["utilidad"].sum()

# ==========================
# Controles
# ==========================

st.sidebar.header("Escenarios")

precio_pct = st.sidebar.slider(
    "Variación Precio %",
    -50,
    50,
    0
)

cantidad_pct = st.sidebar.slider(
    "Variación Cantidad %",
    -50,
    50,
    0
)

margen_pct = st.sidebar.slider(
    "Variación Margen %",
    -50,
    50,
    0
)

# ==========================
# Simulación
# ==========================

factor_precio = (
    1 + precio_pct/100
)

factor_cantidad = (
    1 + cantidad_pct/100
)

factor_margen = (
    1 + margen_pct/100
)

ventas_simuladas = (
    ventas_actuales
    * factor_precio
    * factor_cantidad
)

utilidad_simulada = (
    utilidad_actual
    * factor_margen
)

# ==========================
# KPIs
# ==========================

st.subheader("Resultados")

c1,c2 = st.columns(2)

c1.metric(
    "Ventas Simuladas",
    f"${ventas_simuladas:,.0f}",
    delta=f"{ventas_simuladas-ventas_actuales:,.0f}"
)

c2.metric(
    "Utilidad Simulada",
    f"${utilidad_simulada:,.0f}",
    delta=f"{utilidad_simulada-utilidad_actual:,.0f}"
)

# ==========================
# Comparación
# ==========================

fig = go.Figure()

fig.add_bar(
    name="Actual",
    x=["Ventas","Utilidad"],
    y=[
        ventas_actuales,
        utilidad_actual
    ]
)

fig.add_bar(
    name="Simulado",
    x=["Ventas","Utilidad"],
    y=[
        ventas_simuladas,
        utilidad_simulada
    ]
)

fig.update_layout(
    barmode="group"
)

# st.plotly_chart(
#     fig,
#     width='stretch'
# )

st.plotly_chart(
    fig,
    width='stretch',
    key="whatif_comparacion"
)

# ==========================
# Impacto
# ==========================

st.subheader("Impacto del Escenario")

variacion = (
    (ventas_simuladas - ventas_actuales)
    / ventas_actuales
) * 100

if variacion > 15:

    st.success(
        f"El escenario incrementa las ventas en {variacion:.1f}%."
    )

elif variacion > 0:

    st.info(
        f"El escenario mejora las ventas en {variacion:.1f}%."
    )

else:

    st.warning(
        f"El escenario reduce las ventas en {abs(variacion):.1f}%."
    )

# ==========================
# Forecast ajustado
# ==========================

forecast_90 = ventas_actuales * 0.25

forecast_simulado = (
    forecast_90
    * factor_precio
    * factor_cantidad
)

st.subheader("Forecast Ajustado")

st.metric(
    "Forecast Proyectado",
    f"${forecast_simulado:,.0f}"
)