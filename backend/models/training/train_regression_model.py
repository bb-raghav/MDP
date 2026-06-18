import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..")
)

INPUT_FILE = os.path.join(
    ROOT_DIR,
    "data",
    "processed",
    "aqi_training_data.csv"
)

MODEL_OUTPUT = os.path.join(
    os.path.dirname(__file__),
    "..",
    "saved",
    "aqi_regression_model.pkl"
)

FEATURE_COLUMNS_OUTPUT = os.path.join(
    os.path.dirname(__file__),
    "..",
    "saved",
    "feature_columns.pkl"
)


def train_model():

    print("\nLoading training data...\n")

    df = pd.read_csv(INPUT_FILE)


    # =========================
    # FEATURES / TARGET
    # =========================

    X = df.drop(
        columns=["aqi"]
    )

    y = df["aqi"]


    # =========================
    # TRAIN TEST SPLIT
    # =========================

    X_train, X_test, y_train, y_test = (

        train_test_split(

            X,
            y,

            test_size=0.2,

            random_state=42
        )
    )


    print("=" * 60)
    print("TRAINING SHAPE")
    print("=" * 60)

    print(X_train.shape)

    print("\nTEST SHAPE")

    print(X_test.shape)


    # =========================
    # MODEL
    # =========================

    print("\nTraining model...\n")

    model = RandomForestRegressor(

        n_estimators=200,

        max_depth=15,

        random_state=42,

        n_jobs=-1
    )


    model.fit(

        X_train,
        y_train
    )


    # =========================
    # PREDICTIONS
    # =========================

    predictions = model.predict(
        X_test
    )


    # =========================
    # METRICS
    # =========================

    mae = mean_absolute_error(

        y_test,
        predictions
    )

    r2 = r2_score(

        y_test,
        predictions
    )


    print("\n" + "=" * 60)
    print("MODEL PERFORMANCE")
    print("=" * 60)

    print(f"MAE: {mae:.2f}")

    print(f"R² Score: {r2:.4f}")


    # =========================
    # SAVE MODEL
    # =========================

    joblib.dump(

        model,

        MODEL_OUTPUT
    )

    joblib.dump(
        X.columns.tolist(),
        FEATURE_COLUMNS_OUTPUT
    )


    print("\nModel saved!")
    print(f"Saved to: {MODEL_OUTPUT}")
    print(f"Feature columns saved to: {FEATURE_COLUMNS_OUTPUT}")


if __name__ == "__main__":

    train_model()
