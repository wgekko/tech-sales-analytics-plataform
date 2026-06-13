import pandas as pd
from datetime import datetime

def build_rfm(df):

    fecha_max = df["fecha"].max()

    rfm = (
        df.groupby("producto")
        .agg({
            "fecha": lambda x: (fecha_max - x.max()).days,
            "cantidad": "sum",
            "total": "sum"
        })
    )

    rfm.columns = [
        "Recency",
        "Frequency",
        "Monetary"
    ]

    return rfm