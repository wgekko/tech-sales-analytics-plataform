import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils import load_data
from models.forecast import build_forecast

st.set_page_config(
    page_title="Forecast",
    page_icon=":material/finance:",
    layout="wide"
)

st.subheader(":material/finance: Forecast Center")

df = load_data()

ventas, modelo, features = build_forecast(df)

tab1, tab2, tab3, tab4 = st.tabs([
    " :material/check_box: Forecast",
    " :material/check_box: Backtesting",
    " :material/check_box: Forecast vs Actual",
    " :material/check_box: Modelo"
])

# =====================================================
# TAB 1 FORECAST
# =====================================================

with tab1:

    horizonte = st.selectbox(
        "Horizonte",
        [30,60,90],
        key="forecast_horizonte"
    )

    predicciones = []

    historial = ventas.copy()

    for i in range(horizonte):

        ultima_fecha = historial["fecha"].max()

        nueva_fecha = (
            ultima_fecha +
            pd.Timedelta(days=1)
        )

        nueva_fila = {

            "fecha": nueva_fecha,

            "dia": nueva_fecha.day,

            "mes": nueva_fecha.month,

            "anio": nueva_fecha.year,

            "weekday": nueva_fecha.dayofweek,

            "lag_1":
            historial["total"].iloc[-1],

            "lag_7":
            historial["total"].iloc[-7],

            "lag_14":
            historial["total"].iloc[-14],

            "lag_30":
            historial["total"].iloc[-30],

            "ma_7":
            historial["total"]
            .tail(7)
            .mean(),

            "ma_30":
            historial["total"]
            .tail(30)
            .mean()
        }

        X_pred = pd.DataFrame(
            [nueva_fila]
        )[features]

        pred = modelo.predict(
            X_pred
        )[0]

        nueva_fila["total"] = pred

        historial = pd.concat(
            [
                historial,
                pd.DataFrame(
                    [nueva_fila]
                )
            ],
            ignore_index=True
        )

        predicciones.append(
            {
                "fecha": nueva_fecha,
                "prediccion": pred
            }
        )

    future = pd.DataFrame(
        predicciones
    )

    # ---------------------
    # Tendencia
    # ---------------------

    future["rolling7"] = (
        future["prediccion"]
        .rolling(7)
        .mean()
    )

    # ---------------------
    # Banda Superior
    # ---------------------

    future["upper"] = (
        future["prediccion"]
        * 1.10
    )

    # ---------------------
    # Banda Inferior
    # ---------------------

    future["lower"] = (
        future["prediccion"]
        * 0.90
    )

    # ---------------------
    # KPIs
    # ---------------------

    c1,c2,c3 = st.columns(3)

    c1.metric(
        "Ventas Esperadas",
        f"${future['prediccion'].sum():,.0f}"
    )

    c2.metric(
        "Promedio Diario",
        f"${future['prediccion'].mean():,.0f}"
    )

    c3.metric(
        "Máxima Esperada",
        f"${future['prediccion'].max():,.0f}"
    )

    # ---------------------
    # Gráfico
    # ---------------------

    fig = go.Figure()

    # fig.add_trace(
    #     go.Scatter(
    #         x=ventas["fecha"],
    #         y=ventas["total"],
    #         mode="lines",
    #         name="Histórico"
    #     )
    # )
    #---------- mejora de color de lineas
    # ------- mejora en el color de lineas ---------------------

    fig.add_trace(
        go.Scatter(
            x=ventas["fecha"],
            y=ventas["total"],
            mode="lines",
            name="Histórico",
            line=dict(
                color="#57E71F",
                width=3
            )
        )
    )

    # fig.add_trace(
    #     go.Scatter(
    #         x=future["fecha"],
    #         y=future["prediccion"],
    #         mode="lines",
    #         name="Forecast"
    #     )
    # )

    #------------------------------------------
    fig.add_trace(
        go.Scatter(
            x=future["fecha"],
            y=future["prediccion"],
            mode="lines",
            name="Forecast",
            line=dict(
                color="#FF6B00",
                width=2
            )
        )
    )

    # fig.add_trace(
    #     go.Scatter(
    #         x=future["fecha"],
    #         y=future["rolling7"],
    #         mode="lines",
    #         name="Media Móvil 7 días"
    #     )
    # )

    fig.add_trace(
        go.Scatter(
            x=future["fecha"],
            y=future["rolling7"],
            mode="lines",
            name="Media Móvil 7 días",
            line=dict(
                color="#00A86B",
                dash="dash"
            )
        )
    )

    # fig.add_trace(
    #     go.Scatter(
    #         x=future["fecha"],
    #         y=future["upper"],
    #         mode="lines",
    #         name="Upper Band"
    #     )
    # )

    fig.add_trace(
        go.Scatter(
            x=future["fecha"],
            y=future["upper"],
            mode="lines",
            name="Upper Band",
            line=dict(
                color="#E63946",
                dash="dot"
            )
        )
    )

    # fig.add_trace(
    #     go.Scatter(
    #         x=future["fecha"],
    #         y=future["lower"],
    #         mode="lines",
    #         name="Lower Band"
    #     )
    # )

    fig.add_trace(
        go.Scatter(
            x=future["fecha"],
            y=future["lower"],
            mode="lines",
            name="Lower Band",
            line=dict(
                color="#9D4EDD",
                dash="dot"
            )
        )
    )

    fig.update_layout(
        title="Forecast con Banda de Confianza",
        xaxis_title="Fecha",
        yaxis_title="Ventas"
    )

    st.plotly_chart(
        fig,
        width='stretch',
        key="forecast_principal"
    )

    st.subheader(
        "Predicciones"
    )

    st.dataframe(
        future,
        width='stretch'
    )
# =====================================================
# TAB 2 BACKTESTING
# =====================================================

with tab2:

    historico = ventas.copy()

    historico["pred"] = (
        historico["total"]
        .rolling(7)
        .mean()
    )

    historico = historico.dropna()

    historico["error"] = abs(
        historico["total"]
        -
        historico["pred"]
    )

    historico["error_pct"] = (
        historico["error"]
        /
        historico["total"]
    ) * 100

    mape = historico["error_pct"].mean()

    st.metric(
        "MAPE",
        f"{mape:.2f}%"
    )

#--------- se mejora el color de las lineas del gráfico

    # fig_back = px.line(
    #     historico,
    #     x="fecha",
    #     y=["total","pred"]
    # )
    fig_back = go.Figure()

    fig_back.add_trace(
        go.Scatter(
            x=historico["fecha"],
            y=historico["total"],
            name="Real",
            line=dict(
                color="#1F71C4",
                width=3
            )
        )
    )

    fig_back.add_trace(
        go.Scatter(
            x=historico["fecha"],
            y=historico["pred"],
            name="Forecast",
            line=dict(
                color="#B9560E",
                width=2
            )
        )
    )


    st.plotly_chart(
         fig_back,
         width='stretch',
         key="backtesting_chart"
     )

# =====================================================
# TAB 3 FORECAST VS ACTUAL
# =====================================================

with tab3:

    compare = historico.tail(90)

    fig_compare = go.Figure()
    #---------modifico color de lineas de gráfico -------------
    fig_compare.add_trace(
        go.Scatter(
            x=compare["fecha"],
            y=compare["total"],
            name="Real",
            line=dict(
                color="#70E212",
                width=3
            )
        )
    )

    fig_compare.add_trace(
        go.Scatter(
            x=compare["fecha"],
            y=compare["pred"],
            name="Forecast",
            line=dict(
                color="#FF6B00",
                width=2
            )
        )
    )    

    # fig_compare.add_trace(
    #     go.Scatter(
    #         x=compare["fecha"],
    #         y=compare["total"],
    #         name="Real"
    #     )
    # )

    # fig_compare.add_trace(
    #     go.Scatter(
    #         x=compare["fecha"],
    #         y=compare["pred"],
    #         name="Forecast"
    #     )
    # )

    st.plotly_chart(
        fig_compare,
        width='stretch',
        key="compare_chart"
    )

    st.dataframe(
        compare[
            [
                "fecha",
                "total",
                "pred",
                "error_pct"
            ]
        ],
        width='stretch'
    )

# =====================================================
# TAB 4 MODELO
# =====================================================

with tab4:

    importance = pd.DataFrame({

        "Feature": features,

        "Importance":
        modelo.feature_importances_

    })

    importance = importance.sort_values(
        "Importance",
        ascending=False
    )

    fig_imp = px.bar(
        importance,
        x="Importance",
        y="Feature",
        orientation="h"
    )

    st.plotly_chart(
        fig_imp,
        width='stretch',
        key="importance_chart"
    )

    st.dataframe(
        importance,
        width='stretch'
    )


