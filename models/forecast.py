import pandas as pd

from xgboost import XGBRegressor

# ==================================
# Entrenamiento
# ==================================

def build_forecast(df):

    ventas = (
        df.groupby("fecha")["total"]
        .sum()
        .reset_index()
        .sort_values("fecha")
    )

    ventas["dia"] = ventas["fecha"].dt.day
    ventas["mes"] = ventas["fecha"].dt.month
    ventas["anio"] = ventas["fecha"].dt.year
    ventas["weekday"] = ventas["fecha"].dt.dayofweek

    ventas["lag_1"] = ventas["total"].shift(1)
    ventas["lag_7"] = ventas["total"].shift(7)
    ventas["lag_14"] = ventas["total"].shift(14)
    ventas["lag_30"] = ventas["total"].shift(30)

    ventas["ma_7"] = (
        ventas["total"]
        .rolling(7)
        .mean()
    )

    ventas["ma_30"] = (
        ventas["total"]
        .rolling(30)
        .mean()
    )

    ventas.dropna(inplace=True)

    features = [
        "dia",
        "mes",
        "anio",
        "weekday",
        "lag_1",
        "lag_7",
        "lag_14",
        "lag_30",
        "ma_7",
        "ma_30"
    ]

    X = ventas[features]
    y = ventas["total"]

    model = XGBRegressor(
        n_estimators=500,
        learning_rate=0.03,
        max_depth=5,
        random_state=42
    )

    model.fit(X, y)

    return ventas, model, features


# ==================================
# Forecast futuro
# ==================================

def generate_forecast(
    df,
    horizonte=90
):

    ventas, model, features = (
        build_forecast(df)
    )

    historial = ventas.copy()

    predicciones = []

    for _ in range(horizonte):

        ultima_fecha = (
            historial["fecha"]
            .max()
        )

        nueva_fecha = (
            ultima_fecha
            + pd.Timedelta(days=1)
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

        pred = (
            model.predict(X_pred)[0]
        )

        nueva_fila["total"] = pred

        historial = pd.concat(
            [
                historial,
                pd.DataFrame([nueva_fila])
            ],
            ignore_index=True
        )

        predicciones.append({
            "fecha": nueva_fecha,
            "prediccion": pred
        })

    future = pd.DataFrame(
        predicciones
    )

    return future


# ==================================
# MAPE
# ==================================

def calculate_mape(df):

    ventas, model, features = (
        build_forecast(df)
    )

    X = ventas[features]
    y = ventas["total"]

    pred = model.predict(X)

    mape = (
        abs(
            (y - pred) / y
        )
        .mean()
    )

    return round(
        float(mape),
        4
    )


# ==================================
# Resumen Forecast
# ==================================

def get_forecast_summary(df):

    future30 = (
        generate_forecast(
            df,
            30
        )
    )

    future60 = (
        generate_forecast(
            df,
            60
        )
    )

    future90 = (
        generate_forecast(
            df,
            90
        )
    )

    mape = (
        calculate_mape(df)
    )

    return {

        "forecast_30":
            future30["prediccion"]
            .sum(),

        "forecast_60":
            future60["prediccion"]
            .sum(),

        "forecast_90":
            future90["prediccion"]
            .sum(),

        "mape":
            mape
    }


# import pandas as pd
# from xgboost import XGBRegressor

# def build_forecast(df):

#     ventas = (
#         df.groupby("fecha")["total"]
#         .sum()
#         .reset_index()
#         .sort_values("fecha")
#     )

#     ventas["dia"] = ventas["fecha"].dt.day
#     ventas["mes"] = ventas["fecha"].dt.month
#     ventas["anio"] = ventas["fecha"].dt.year
#     ventas["weekday"] = ventas["fecha"].dt.dayofweek

#     ventas["lag_1"] = ventas["total"].shift(1)
#     ventas["lag_7"] = ventas["total"].shift(7)
#     ventas["lag_14"] = ventas["total"].shift(14)
#     ventas["lag_30"] = ventas["total"].shift(30)

#     ventas["ma_7"] = ventas["total"].rolling(7).mean()
#     ventas["ma_30"] = ventas["total"].rolling(30).mean()

#     ventas.dropna(inplace=True)

#     features = [
#         "dia",
#         "mes",
#         "anio",
#         "weekday",
#         "lag_1",
#         "lag_7",
#         "lag_14",
#         "lag_30",
#         "ma_7",
#         "ma_30"
#     ]

#     X = ventas[features]
#     y = ventas["total"]

#     model = XGBRegressor(
#         n_estimators=500,
#         learning_rate=0.03,
#         max_depth=5,
#         random_state=42
#     )

#     model.fit(X, y)

#     return ventas, model, features