from pathlib import Path
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression

def train_model() -> None:
    """
    Train a Logistic Regression model on the Iris training dataset and save it.

    Reads:
        dataset/iris_train.csv
    Writes:
        model.pkl
    """
    base_dir = Path(__file__).parent
    dataset_dir = base_dir / "dataset"
    train_df = pd.read_csv(dataset_dir / "iris_train.csv")
    X_train = train_df.drop(columns=["target"])
    y_train = train_df["target"]
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    joblib.dump(model, base_dir / "model.pkl") 