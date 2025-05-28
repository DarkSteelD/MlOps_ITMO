from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, roc_auc_score
from sklearn.preprocessing import label_binarize
import numpy as np
from clearml import Task

from config import config
from data import get_data


def train(model, x_train, y_train) -> None:
    model.fit(x_train, y_train)


def test(model, x_test, y_test) -> None:
    y_pred = model.predict(x_test)
    y_pred_proba = model.predict_proba(x_test)
    
    accuracy = accuracy_score(y_true=y_test, y_pred=y_pred)
    f1 = f1_score(y_true=y_test, y_pred=y_pred, average='weighted')
    conf_matrix = confusion_matrix(y_true=y_test, y_pred=y_pred)
    
    y_test_binarized = label_binarize(y_test, classes=np.unique(y_test))
    if y_test_binarized.shape[1] == 1:
        auc_roc = roc_auc_score(y_test, y_pred_proba[:, 1])
    else:
        auc_roc = roc_auc_score(y_test_binarized, y_pred_proba, multi_class='ovr', average='weighted')
    
    logger = Task.current_task().get_logger()
    logger.report_scalar("Metrics", "Accuracy", value=accuracy, iteration=0)
    logger.report_scalar("Metrics", "F1 Score", value=f1, iteration=0)
    logger.report_scalar("Metrics", "AUC-ROC", value=auc_roc, iteration=0)
    logger.report_confusion_matrix("Confusion Matrix", "ignored", iteration=0, matrix=conf_matrix)
    
    print(f"Accuracy: {accuracy}")
    print(f"F1 Score: {f1}")
    print(f"AUC-ROC: {auc_roc}")


if __name__ == "__main__":
    task = Task.init(project_name="MLOps Lesson 4", task_name="Logistic Regression - Digits Classification")
    
    task.connect(config)
    
    logistic_regression_model = LogisticRegression(
        max_iter=config["logistic_regression"]["max_iter"],
        random_state=config["random_state"]
    )
    
    model_params = {
        "model_type": "LogisticRegression",
        "max_iter": config["logistic_regression"]["max_iter"],
        "random_state": config["random_state"],
        "solver": logistic_regression_model.solver,
        "penalty": logistic_regression_model.penalty,
        "C": logistic_regression_model.C
    }
    task.connect(model_params, name="model_parameters")

    data = get_data()
    train(logistic_regression_model, data["x_train"], data["y_train"])
    
    coefficients_info = {
        "n_features": logistic_regression_model.coef_.shape[1],
        "n_classes": logistic_regression_model.coef_.shape[0],
        "intercept_shape": logistic_regression_model.intercept_.shape
    }
    task.connect(coefficients_info, name="model_coefficients_info")
    
    test(logistic_regression_model, data["x_test"], data["y_test"])
