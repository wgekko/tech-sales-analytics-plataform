from sklearn.preprocessing import MinMaxScaler

def ranking_productos(df):

    ranking = (
        df.groupby("producto")
        .agg({
            "total":"sum",
            "utilidad":"sum",
            "cantidad":"sum"
        })
    )

    scaler = MinMaxScaler()

    ranking[[
        "ventas_n",
        "utilidad_n",
        "cantidad_n"
    ]] = scaler.fit_transform(
        ranking
    )

    ranking["score"] = (
        ranking["ventas_n"]*0.4 +
        ranking["utilidad_n"]*0.4 +
        ranking["cantidad_n"]*0.2
    )

    return ranking.sort_values(
        "score",
        ascending=False
    )