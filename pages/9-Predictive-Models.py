import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from utils import load_data
from models.predictive import train_models


st.set_page_config(
    page_title="Predictive Models",
    page_icon=":material/graph_3:",
    layout="wide"
)

st.subheader(":material/graph_3: XGBoost vs Random Forest")

df = load_data()

# ======================
# Ventas por fecha
# ======================

ventas = (
    df.groupby("fecha")
      ["total"]
      .sum()
      .reset_index()
)

ventas["dia"] = ventas["fecha"].dt.day
ventas["mes"] = ventas["fecha"].dt.month
ventas["anio"] = ventas["fecha"].dt.year
ventas["weekday"] = ventas["fecha"].dt.dayofweek

# ======================
# Features
# ======================

X = ventas[
    ["dia","mes","anio","weekday"]
]

y = ventas["total"]

# ======================
# Train/Test
# ======================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# ======================
# Modelos
# ======================

rf, xgb = train_models(
    X_train,
    y_train
)

# ======================
# Predicciones
# ======================

pred_rf = rf.predict(X_test)

pred_xgb = xgb.predict(X_test)

# ======================
# Métricas RF
# ======================

rf_mae = mean_absolute_error(
    y_test,
    pred_rf
)

rf_r2 = r2_score(
    y_test,
    pred_rf
)

# ======================
# Métricas XGB
# ======================

xgb_mae = mean_absolute_error(
    y_test,
    pred_xgb
)

xgb_r2 = r2_score(
    y_test,
    pred_xgb
)

# ======================
# KPIs
# ======================

st.subheader("Resultados")

c1,c2 = st.columns(2)

with c1:
    st.metric(
        "RF MAE",
        f"{rf_mae:,.2f}"
    )

    st.metric(
        "RF R²",
        f"{rf_r2:.3f}"
    )

with c2:
    st.metric(
        "XGB MAE",
        f"{xgb_mae:,.2f}"
    )

    st.metric(
        "XGB R²",
        f"{xgb_r2:.3f}"
    )

# ======================
# Ganador
# ======================

if xgb_r2 > rf_r2:
    st.success(":material/trophy: XGBoost obtiene mejor desempeño")
else:
    st.success(":material/trophy: Random Forest obtiene mejor desempeño")

# ======================
# Comparación gráfica
# ======================

resultados = pd.DataFrame({
    "Real": y_test.values,
    "Random Forest": pred_rf,
    "XGBoost": pred_xgb
})

fig = go.Figure()

#--------- modificación de color lineas de gráficos -------------

fig.add_trace(
    go.Scatter(
        y=resultados["Real"],
        mode="lines",
        name="Real",
        line=dict(
            color="#1D6E0D",
            width=3
        )
    )
)

# fig.add_trace(
#     go.Scatter(
#         y=resultados["Real"],
#         mode="lines",
#         name="Real"
#     )
# )

fig.add_trace(
    go.Scatter(
        y=resultados["Random Forest"],
        mode="lines",
        name="RF"
    )
)

fig.add_trace(
    go.Scatter(
        y=resultados["XGBoost"],
        mode="lines",
        name="XGB",
            line=dict(
            color="#6C26EC",
            width=3
        )
    )
)

st.plotly_chart(
    fig,
    width='stretch'
)

# ======================
# Tabla
# ======================

st.subheader("Detalle")

st.dataframe(resultados)