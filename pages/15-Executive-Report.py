import streamlit as st
import pandas as pd
import plotly.express as px
from utils_pdf import ( generate_executive_pdf)

from utils import load_data

from models.forecast import (
    get_forecast_summary
)

st.set_page_config(
    page_title="Executive Report",
    page_icon=":material/breaking_news:",
    layout="wide"
)

st.subheader(":material/breaking_news: Executive Report")

df = load_data()

# ==================================
# KPIs PRINCIPALES
# ==================================

ventas = df["total"].sum()

utilidad = df["utilidad"].sum()

margen = (
    utilidad / ventas
) * 100

productos = (
    df["producto"]
    .nunique()
)

# ==================================
# FORECAST
# ==================================

summary = get_forecast_summary(df)

forecast30 = summary["forecast_30"]
forecast60 = summary["forecast_60"]
forecast90 = summary["forecast_90"]

mape = summary["mape"]

# ==================================
# BUSINESS HEALTH
# ==================================

score = 0

score += min(
    ventas / 1_000_000 * 25,
    25
)

score += min(
    margen,
    25
)

score += 25

score += 20

score = round(score,1)

# ==================================
# KPIs
# ==================================

st.subheader("KPIs Ejecutivos")

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Ventas",
    f"${ventas:,.0f}"
)

c2.metric(
    "Utilidad",
    f"${utilidad:,.0f}"
)

c3.metric(
    "Margen",
    f"{margen:.2f}%"
)

c4.metric(
    "Business Score",
    f"{score}/100"
)

# ==================================
# FORECAST
# ==================================

st.subheader("Forecast Ejecutivo")

c1,c2,c3 = st.columns(3)

c1.metric(
    "30 días",
    f"${forecast30:,.0f}"
)

c2.metric(
    "60 días",
    f"${forecast60:,.0f}"
)

c3.metric(
    "90 días",
    f"${forecast90:,.0f}"
)

# ==================================
# TOP PRODUCTOS
# ==================================

st.subheader("Top Productos")

top = (
    df.groupby("producto")
        ["total"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
        .reset_index()
)

fig = px.bar(
    top,
    x="total",
    y="producto",
    orientation="h",
    title="Top 10 Productos"
)

st.plotly_chart(
    fig,
    width='stretch',
    key="exec_top_productos"
)

# ==================================
# TOP CATEGORIAS
# ==================================

st.subheader("Categorías")

cat = (
    df.groupby("categoria")
      ["total"]
      .sum()
      .reset_index()
)

fig2 = px.pie(
    cat,
    names="categoria",
    values="total",
    title="Participación por Categoría"
)

st.plotly_chart(
    fig2,
    width='stretch',
    key="exec_categorias"
)

# ==================================
# RESUMEN EJECUTIVO
# ==================================

producto_top = (
    df.groupby("producto")
        ["total"]
        .sum()
        .idxmax()
)

categoria_top = (
    df.groupby("categoria")
        ["total"]
        .sum()
        .idxmax()
)

pais_top = (
    df.groupby("pais")
        ["total"]
        .sum()
        .idxmax()
)

st.subheader("Resumen Ejecutivo")

st.success(f"""
Ventas acumuladas por ${ventas:,.0f}.

La utilidad alcanza ${utilidad:,.0f}.

El margen consolidado es de {margen:.2f}%.

El producto líder es:

{producto_top}

La categoría líder es:

{categoria_top}

El país con mayor facturación es:

{pais_top}

El forecast proyecta ventas por
${forecast90:,.0f}
durante los próximos 90 días.
""")

# ==================================
# INSIGHTS
# ==================================

st.subheader("Insights Automáticos")

if margen > 25:

    st.success(
        "La rentabilidad se encuentra en niveles elevados."
    )

elif margen > 15:

    st.info(
        "La rentabilidad es saludable."
    )

else:

    st.warning(
        "La rentabilidad requiere revisión."
    )

if forecast90 > ventas:

    st.success(
        "El forecast proyecta crecimiento."
    )

else:

    st.warning(
        "El forecast anticipa desaceleración."
    )

if top["total"].iloc[0] > ventas * 0.25:

    st.warning(
        "Existe dependencia significativa de un producto."
    )

# ==================================
# RECOMENDACIONES
# ==================================

st.subheader("Recomendaciones")

st.info(f"""
• Incrementar disponibilidad de {producto_top}

• Reforzar campañas de {categoria_top}

• Consolidar operaciones en {pais_top}

• Mantener monitoreo del Forecast

• Revisar productos de bajo margen
""")

# ==================================
# PDF
# ==================================

st.subheader("Exportación")

resumen = [

    f"Ventas: ${ventas:,.0f}",

    f"Utilidad: ${utilidad:,.0f}",

    f"Margen: {margen:.2f}%",

    f"Forecast 30 días: ${forecast30:,.0f}",

    f"Forecast 60 días: ${forecast60:,.0f}",

    f"Forecast 90 días: ${forecast90:,.0f}",

    f"Producto líder: {producto_top}",

    f"Categoría líder: {categoria_top}",

    f"País líder: {pais_top}",

    f"Business Score: {score}/100"

]

if st.button(
    ":material/picture_as_pdf: Generar Executive Report PDF"
):

    pdf_file = generate_executive_pdf(
        "Executive_Report.pdf",
        resumen
    )

    with open(
        pdf_file,
        "rb"
    ) as file:

        st.download_button(
            label="⬇ Descargar PDF",
            data=file,
            file_name="Executive_Report.pdf",
            mime="application/pdf"
        )


# if st.button(
#     ":material/picture_as_pdf: Generar Executive Report PDF"
# ):

#     st.info(
#         "Próxima versión: generación automática de PDF."
#     )

# ==================================
# CALIDAD MODELO
# ==================================

st.subheader("Calidad Predictiva")

st.metric(
    "MAPE",
    f"{mape:.2%}"
)



# import streamlit as st
# 
# from utils import load_data
# 
# st.set_page_config(
    # page_title="Executive Report",
    # page_icon=":material/article:",
    # layout="wide"
# )
# 
# st.subheader(":material/article: Executive Report")
# 
# df = load_data()
# 
# ventas = df["total"].sum()
# 
# utilidad = df["utilidad"].sum()
# 
# margen = (
    # utilidad /
    # ventas
# ) * 100
# 
# producto_top = (
    # df.groupby("producto")
    #   ["total"]
    #   .sum()
    #   .idxmax()
# )
# 
# categoria_top = (
    # df.groupby("categoria")
    #   ["total"]
    #   .sum()
    #   .idxmax()
# )
# 
# pais_top = (
    # df.groupby("pais")
    #   ["total"]
    #   .sum()
    #   .idxmax()
# )
# 
# st.success(f"""
# 
#Resumen Ejecutivo
# 
# - Ventas Totales:
# ${ventas:,.0f}
# 
# - Utilidad:
# ${utilidad:,.0f}
# 
# - Producto Líder:
# {producto_top}
# 
# - Categoría Líder:
# {categoria_top}
# 
# - País Líder:
# {pais_top}
# 
# - Margen:
# {margen:.2f}%
# 
# """)
# 
#=========================
#Diagnóstico
#=========================
# 
# st.subheader(":material/clinical_notes: Diagnóstico")
# 
# if margen > 25:
# 
    # st.success(
        # "Rentabilidad excelente."
    # )
# 
# elif margen > 15:
# 
    # st.info(
        # "Rentabilidad saludable."
    # )
# 
# else:
# 
    # st.warning(
        # "Rentabilidad baja."
    # )
# 
#=========================
#Recomendaciones
#=========================
# 
# st.subheader(":material/share_reviews: Recomendaciones")
# 
# st.info(f"""
# 
# 1. Incrementar disponibilidad de:
# 
# {producto_top}
# 
# 2. Reforzar campañas de:
# 
# {categoria_top}
# 
# 3. Expandir presencia en:
# 
# {pais_top}
# 
# 4. Monitorear categorías de bajo margen.
# 
# 5. Mantener seguimiento del forecast.
# """)
# 
#=========================
#Score Ejecutivo
#=========================
# 
# score = 0
# 
# score += min(
    # ventas / 1000000 * 25,
    # 25
# )
# 
# score += min(
    # margen,
    # 25
# )
# 
# score += 25
# 
# score += 20
# 
# score = round(score,1)
# 
# st.metric(
    # "Executive Score",
    # f"{score}/100"
# )