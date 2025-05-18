from pathlib import Path
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

def load_data() -> None:
    """
    Load the Iris dataset from sklearn and save it as a CSV file.

    Saves:
        dataset/iris.csv
    """
    dataset_dir = Path(__file__).parent / "dataset"
    dataset_dir.mkdir(parents=True, exist_ok=True)
    iris = load_iris(as_frame=True)
    df = iris.frame
    df.to_csv(dataset_dir / "iris.csv", index=False)

def prepare_data(test_size: float = 0.2, random_state: int = 42) -> None:
    """
    Load iris.csv and split into training and test sets.

    Args:
        test_size: Proportion of the dataset to include in the test split.
        random_state: Seed used by the random number generator.

    Saves:
        dataset/iris_train.csv
        dataset/iris_test.csv
    """
    dataset_dir = Path(__file__).parent / "dataset"
    df = pd.read_csv(dataset_dir / "iris.csv")
    X = df.drop(columns=["target"])
    y = df["target"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    train_df = pd.concat([X_train, y_train], axis=1)
    test_df = pd.concat([X_test, y_test], axis=1)
    train_df.to_csv(dataset_dir / "iris_train.csv", index=False)
    test_df.to_csv(dataset_dir / "iris_test.csv", index=False) 