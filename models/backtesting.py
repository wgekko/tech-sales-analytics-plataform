import pandas as pd
import numpy as np

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    mean_absolute_percentage_error
)

from xgboost import XGBRegressor


def walk_forward_validation(
    ventas,
    features,
    train_size=0.80
):

    split = int(len(ventas) * train_size)

    train = ventas.iloc[:split].copy()

    test = ventas.iloc[split:].copy()

    preds = []

    reales = []

    historial = train.copy()

    for i in range(len(test)):

        X_train = historial[features]

        y_train = historial["total"]

        model = XGBRegressor(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=5,
            random_state=42
        )

        model.fit(X_train, y_train)

        fila = test.iloc[[i]]

        pred = model.predict(
            fila[features]
        )[0]

        real = fila["total"].values[0]

        preds.append(pred)

        reales.append(real)

        historial = pd.concat(
            [historial, fila]
        )

    mae = mean_absolute_error(
        reales,
        preds
    )

    rmse = np.sqrt(
        mean_squared_error(
            reales,
            preds
        )
    )

    mape = mean_absolute_percentage_error(
        reales,
        preds
    )

    r2 = r2_score(
        reales,
        preds
    )

    return {
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape,
        "R2": r2,
        "preds": preds,
        "reales": reales
    }


