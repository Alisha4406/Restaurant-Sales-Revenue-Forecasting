from sklearn.ensemble import GradientBoostingRegressor
import joblib

def train_model(X_train, y_train):

    model = GradientBoostingRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=5,
        random_state=42
    )

    model.fit(X_train, y_train)

    return model


def save_model(model, path):

    joblib.dump(model, path)


def load_model(path):

    return joblib.load(path)