from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

def train_models(X,y):

    rf = RandomForestRegressor(
        n_estimators=300,
        random_state=42
    )

    xgb = XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=5,
        random_state=42
    )

    rf.fit(X,y)
    xgb.fit(X,y)

    return rf,xgb