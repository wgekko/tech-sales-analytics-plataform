from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score


def run_kmeans(df, group_col):

    data = (
        df.groupby(group_col)
        .agg({
            "cantidad":"sum",
            "total":"sum",
            "utilidad":"sum"
        })
    )

    scaler = StandardScaler()

    X = scaler.fit_transform(data)

    # model = KMeans(
    #     n_clusters=4,
    #     random_state=42,
    #     n_init=10
    # )

    for k in range(2,10):

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

    score = silhouette_score(
        X,
        model.fit_predict(X)
    )

    data["cluster"] = model.fit_predict(X)

    pca = PCA(n_components=2)

    coords = pca.fit_transform(X)

    data["x"] = coords[:,0]
    data["y"] = coords[:,1]

    return data

def encontrar_mejor_k(X):

    mejor_k = 2
    mejor_score = -1

    for k in range(2,10):

        modelo = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        labels = modelo.fit_predict(X)

        score = silhouette_score(
            X,
            labels
        )

        if score > mejor_score:

            mejor_score = score
            mejor_k = k

    return mejor_k


