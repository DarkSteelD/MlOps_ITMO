from pathlib import Path
import pandas as pd
import joblib
import json
from sklearn.metrics import accuracy_score, classification_report

def test_model() -> None:
    """
    Test the trained model on the Iris test dataset and save evaluation metrics.

    Reads:
        dataset/iris_test.csv
        model.pkl
    Writes:
        model_metrics.json
    """
    base_dir = Path(__file__).parent
    dataset_dir = base_dir / "dataset"
    test_df = pd.read_csv(dataset_dir / "iris_test.csv")
    X_test = test_df.drop(columns=["target"])
    y_test = test_df["target"]
    model = joblib.load(base_dir / "model.pkl")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    metrics = {"accuracy": accuracy, "report": report}
    with open(base_dir / "model_metrics.json", "w") as f:
        json.dump(metrics, f) 