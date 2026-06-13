import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_data

from models.forecast import (
    get_forecast_summary
)

st.set_page_config(
    page_title="AI Insights",
    page_icon=":material/search_insights:",
    layout="wide"
)

st.subheader(":material/search_insights: AI Insights Center")

# =====================================================
# DATOS
# =====================================================

df = load_data()

ventas = df["total"].sum()

utilidad = df["utilidad"].sum()

margen = (
    utilidad / ventas
) * 100

producto_top = (
    df.groupby("producto")["total"]
    .sum()
    .idxmax()
)

categoria_top = (
    df.groupby("categoria")["total"]
    .sum()
    .idxmax()
)

pais_top = (
    df.groupby("pais")["total"]
    .sum()
    .idxmax()
)

# =====================================================
# FORECAST REAL
# =====================================================

summary = get_forecast_summary(df)

forecast30 = summary["forecast_30"]
forecast60 = summary["forecast_60"]
forecast90 = summary["forecast_90"]

# =====================================================
# MÉTRICAS EJECUTIVAS
# =====================================================

ventas_categoria = (
    df.groupby("categoria")["total"]
      .sum()
      .sort_values(ascending=False)
)

participacion_categoria = (
    ventas_categoria.iloc[0]
    / ventas
) * 100

ventas_producto = (
    df.groupby("producto")["total"]
      .sum()
      .sort_values(ascending=False)
)

participacion_producto = (
    ventas_producto.iloc[0]
    / ventas
) * 100

ventas_pais = (
    df.groupby("pais")["total"]
      .sum()
      .sort_values(ascending=False)
)

participacion_pais = (
    ventas_pais.iloc[0]
    / ventas
) * 100

crecimiento_esperado = (
    (forecast90 - ventas)
    / ventas
) * 100

# ==========================================
# NIVEL DE CONCENTRACIÓN
# ==========================================

if participacion_producto > 40:

    riesgo_producto = "Alta"

elif participacion_producto > 25:

    riesgo_producto = "Moderada"

else:

    riesgo_producto = "Baja"



# =====================================================
# PARTICIPACIÓN PRODUCTO TOP
# =====================================================

top_producto_pct = (

    df.groupby("producto")["total"]
      .sum()
      .max()

    / ventas

) * 100

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4 = st.tabs(
    [
        ":material/menu_open: Insights",
        ":material/menu_open: Ejecutivo",
        ":material/menu_open: Estrategia",
        ":material/menu_open: Acciones"
    ]
)

# =====================================================
# TAB 1
# =====================================================

with tab1:

    st.subheader(
        "Hallazgos Automáticos"
    )

    c1,c2,c3 = st.columns(3)

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

    st.success(
        f"""
Producto líder: {producto_top}

Categoría líder: {categoria_top}

País líder: {pais_top}
"""
    )

# =====================================================
# TAB 2
# =====================================================

with tab2:

    st.subheader(
        "Resumen Ejecutivo"
    )

    diagnostico = []

    if margen > 25:

        diagnostico.append(
            "Rentabilidad excelente."
        )

    elif margen > 15:

        diagnostico.append(
            "Rentabilidad saludable."
        )

    else:

        diagnostico.append(
            "Margen por debajo del objetivo."
        )

    if ventas > 1_000_000:

        diagnostico.append(
            "Escala comercial elevada."
        )

    for d in diagnostico:

        st.info(d)

    st.divider()

    st.subheader(
        ":material/neurology: Resumen CFO"
    )

    insights = []

    if margen > 25:

        insights.append(
            "La rentabilidad se encuentra en niveles excelentes."
        )

    elif margen > 15:

        insights.append(
            "La rentabilidad mantiene una tendencia saludable."
        )

    else:

        insights.append(
            "La rentabilidad requiere revisión."
        )

    if forecast90 > ventas:

        insights.append(
            "El forecast proyecta crecimiento para el próximo trimestre."
        )

    else:

        insights.append(
            "El forecast anticipa desaceleración comercial."
        )

    if top_producto_pct > 30:

        insights.append(
            "Existe dependencia significativa de un producto."
        )

    else:

        insights.append(
            "La cartera de productos presenta buena diversificación."
        )

    for i in insights:

        st.success(i)

    st.divider()
    # ==================================
    # CFO COPILOT
    # ==================================

    st.subheader(
        ":material/cognition_2: CFO Copilot"
    )

    riesgos = []
    oportunidades = []
    acciones = []

    # =========================
    # RIESGOS
    # =========================

    if participacion_producto > 40:
        riesgos.append(
            f"Alta dependencia del producto {producto_top}."
        )

    elif participacion_producto > 25:
        riesgos.append(
            f"Dependencia moderada del producto {producto_top}."
    )

    # if top_producto_pct > 30:

    #     riesgos.append(
    #         f"Dependencia elevada del producto {producto_top}."
    #     )

    if margen < 15:
        riesgos.append(
            "Margen operativo por debajo del objetivo."
        )

    if crecimiento_esperado < 0:
        riesgos.append(
            "Se proyecta una desaceleración comercial."
        )

    # if forecast90 < ventas:   ## modificacion de calculo

    #     riesgos.append(
    #         "El forecast anticipa desaceleración comercial."
    #     )

    # =========================
    # OPORTUNIDADES
    # =========================

    if margen > 25:

        oportunidades.append(
            "Rentabilidad superior al promedio."
        )

    if forecast90 > ventas:

        oportunidades.append(
            "El forecast proyecta crecimiento para el próximo trimestre."
        )

    oportunidades.append(
        f"La categoría {categoria_top} lidera la generación de ingresos."
    )

    oportunidades.append(
        f"{pais_top} representa el principal mercado comercial."
    )

    # =========================
    # ACCIONES
    # =========================

    acciones.append(
        f"Aumentar disponibilidad de {producto_top}."
    )

    acciones.append(
        f"Fortalecer campañas comerciales de {categoria_top}."
    )

    acciones.append(
        f"Consolidar operaciones en {pais_top}."
    )

    if margen < 20:

        acciones.append(
            "Revisar estructura de precios para mejorar márgenes."
        )

    if top_producto_pct > 30:

        acciones.append(
            "Reducir dependencia mediante diversificación del portafolio."
        )

    # =========================
    # VISUALIZACIÓN
    # =========================

    c1, c2, c3 = st.columns(3)

    with c1:

        st.error(":material/problem: Riesgos")

        if len(riesgos) == 0:

            st.success(
                "No se detectan riesgos relevantes."
            )

        else:

            for r in riesgos:

                st.write(f"• {r}")

    with c2:

        st.success(":material/manage_search: Oportunidades")

        for o in oportunidades:

            st.write(f"• {o}")

    with c3:

        st.info(":material/contextual_token_add: Acciones Recomendadas")

        for a in acciones:

            st.write(f"• {a}")

    st.divider()

    st.subheader(
        ":material/content_paste_go: Narrativa Ejecutiva"
    )

    st.markdown(
        f"""
        ### Resumen Ejecutivo

        Las ventas acumuladas alcanzan
        **${ventas:,.0f}**.

        La utilidad consolidada asciende a
        **${utilidad:,.0f}**.

        El margen operativo se ubica en
        **{margen:.2f}%**.

        La categoría líder es
        **{categoria_top}**
        y representa el
        **{participacion_categoria:.1f}%**
        de las ventas totales.

        El producto líder es
        **{producto_top}**
        y concentra el
        **{participacion_producto:.1f}%**
        de la facturación.

        El principal mercado es
        **{pais_top}**
        con una participación del
        **{participacion_pais:.1f}%**
        de los ingresos.

        El forecast proyecta ventas por
        **${forecast90:,.0f}**
        durante los próximos 90 días.

        La expectativa de crecimiento es de
        **{crecimiento_esperado:.1f}%**.

        El nivel de concentración comercial
        se clasifica como
        **{riesgo_producto}**.
        """
        )
    
    
    # ------------ opcion  en la interpretación de los datos 

    # st.markdown(
    #     f"""
    # ### Resumen Ejecutivo

    # Las ventas acumuladas alcanzan
    # **${ventas:,.0f}**.

    # La utilidad consolidada asciende a
    # **${utilidad:,.0f}**.

    # El margen operativo se ubica en
    # **{margen:.2f}%**.

    # La categoría con mayor contribución es
    # **{categoria_top}**.

    # El producto líder del período es
    # **{producto_top}**.

    # El principal mercado es
    # **{pais_top}**.

    # El forecast proyecta ventas por
    # **${forecast90:,.0f}**
    # durante los próximos 90 días.

    # La organización presenta una posición comercial sólida, con oportunidades de crecimiento apoyadas en las categorías líderes y en la optimización continua de la rentabilidad.
    # """
    #     )

#--------------------- version anterior -------------------------------------------------

    # st.subheader(
    #     "Narrativa Ejecutiva"
    # )

    # st.markdown(
    #     f"""
    #     ### Resumen CFO

    #     Las ventas acumuladas alcanzan **${ventas:,.0f}**.

    #     La utilidad consolidada asciende a
    #     **${utilidad:,.0f}**.

    #     El margen operativo es de
    #     **{margen:.2f}%**.

    #     La categoría líder es
    #     **{categoria_top}**.

    #     El producto líder es
    #     **{producto_top}**.

    #     El país con mayor contribución es
    #     **{pais_top}**.

    #     El forecast proyecta ventas por
    #     **${forecast90:,.0f}**
    #     durante los próximos 90 días.
    #     """
    #         )

#------------------------ fin de la version anterior ------------------

# =====================================================
# TAB 3
# =====================================================

with tab3:

    st.subheader(
        "Recomendaciones Estratégicas"
    )

    recomendaciones = [

        f"Incrementar disponibilidad de {producto_top}",

        f"Fortalecer campañas de {categoria_top}",

        f"Expandir operaciones en {pais_top}",

        "Monitorear productos de baja rotación",

        "Optimizar categorías de bajo margen"

    ]

    for r in recomendaciones:

        st.write(
            f"✔ {r}"
        )

    fig = px.pie(
        df,
        names="categoria",
        values="total",
        title="Participación por Categoría"
    )

    st.plotly_chart(
        fig,
        width='stretch',
        key="estrategia_categoria"
    )

    st.subheader(
    ":material/network_intel_node: Recomendaciones Inteligentes"
)

    recomendacion = []

    if participacion_producto > 40:

        recomendacion.append(
            f"Diversificar ingresos para reducir dependencia de {producto_top}."
        )

    if margen < 20:

        recomendacion.append(
            "Revisar estructura de precios para mejorar rentabilidad."
        )

    if crecimiento_esperado > 10:

        recomendaciones.append(
            "Incrementar inventario para soportar crecimiento esperado."
        )

    if crecimiento_esperado < 0:

        recomendacion.append(
            "Fortalecer promociones y campañas comerciales."
        )

    recomendacion.append(
        f"Potenciar la categoría {categoria_top}."
    )

    recomendacion.append(
        f"Expandir operaciones en {pais_top}."
    )

    for r in recomendacion:

        st.success(r)



# =====================================================
# TAB 4
# =====================================================

with tab4:

    st.subheader(
        "Plan de Acción"
    )

    acciones = pd.DataFrame({

        "Prioridad":[
            "Alta",
            "Alta",
            "Media",
            "Media",
            "Baja"
        ],

        "Acción":[
            "Aumentar stock",
            "Incrementar campañas",
            "Revisar márgenes",
            "Reducir sobrestock",
            "Analizar nuevos mercados"
        ]

    })

    st.dataframe(
        acciones,
        width='stretch'
    )

    fig = px.pie(
        acciones,
        names="Prioridad",
        title="Distribución de Acciones"
    )

    st.plotly_chart(
        fig,
        width='stretch',
        key="acciones_pie"
    )



# df = load_data()

# ventas = df["total"].sum()

# utilidad = df["utilidad"].sum()

# margen = (
#     utilidad / ventas
# ) * 100

# producto_top = (
#     df.groupby("producto")["total"]
#     .sum()
#     .idxmax()
# )

# categoria_top = (
#     df.groupby("categoria")["total"]
#     .sum()
#     .idxmax()
# )

# pais_top = (
#     df.groupby("pais")["total"]
#     .sum()
#     .idxmax()
# )

# tab1, tab2, tab3, tab4 = st.tabs(
#     [
#         " - Insights",
#         " - Ejecutivo",
#         " - Estrategia",
#         " - Acciones"
#     ]
# )

# # =====================================================
# # INSIGHTS
# # =====================================================

# with tab1:

#     st.subheader(
#         "Hallazgos Automáticos"
#     )

#     c1,c2,c3 = st.columns(3)

#     c1.metric(
#         "Ventas",
#         f"${ventas:,.0f}"
#     )

#     c2.metric(
#         "Utilidad",
#         f"${utilidad:,.0f}"
#     )

#     c3.metric(
#         "Margen",
#         f"{margen:.2f}%"
#     )

#     st.success(
#         f"""
# Producto líder: {producto_top}

# Categoría líder: {categoria_top}

# País líder: {pais_top}
# """
#     )

# # =====================================================
# # EJECUTIVO
# # =====================================================

# with tab2:

#     st.subheader(
#         "Resumen Ejecutivo"
#     )

#     diagnostico = []

#     if margen > 25:

#         diagnostico.append(
#             "Rentabilidad excelente."
#         )

#     elif margen > 15:

#         diagnostico.append(
#             "Rentabilidad saludable."
#         )

#     else:

#         diagnostico.append(
#             "Margen por debajo del objetivo."
#         )

#     if ventas > 1000000:

#         diagnostico.append(
#             "Escala comercial elevada."
#         )

#     for d in diagnostico:

#         st.info(d)

# # =====================================================
# # ESTRATEGIA
# # =====================================================

# with tab3:

#     st.subheader(
#         "Recomendaciones Estratégicas"
#     )

#     recomendaciones = [

#         f"Incrementar disponibilidad de {producto_top}",

#         f"Fortalecer campañas en {categoria_top}",

#         f"Expandir operaciones en {pais_top}",

#         "Monitorear productos de baja rotación",

#         "Optimizar categorías de bajo margen"

#     ]

#     for r in recomendaciones:

#         st.write(
#             f"✔ {r}"
#         )

# # =====================================================
# # ACCIONES
# # =====================================================

# with tab4:

#     st.subheader(
#         "Plan de Acción"
#     )

#     acciones = pd.DataFrame({

#         "Prioridad":[
#             "Alta",
#             "Alta",
#             "Media",
#             "Media",
#             "Baja"
#         ],

#         "Acción":[
#             "Aumentar stock",
#             "Incrementar campañas",
#             "Revisar márgenes",
#             "Reducir sobrestock",
#             "Analizar nuevos mercados"
#         ]
#     })

#     st.dataframe(
#         acciones,
#         width='stretch'
#     )

#     fig = px.pie(
#         acciones,
#         names="Prioridad"
#     )

#     st.plotly_chart(
#         fig,
#         width='stretch',
#         key="acciones_pie"
#     )



