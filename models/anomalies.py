from sklearn.ensemble import IsolationForest

def detect_anomalies(df):

    X = df[
        [
            "cantidad",
            "precio",
            "total",
            "utilidad"
        ]
    ]

    model = IsolationForest(
        contamination=0.02,
        random_state=42
    )

    df["anomalia"] = model.fit_predict(X)

    return df


