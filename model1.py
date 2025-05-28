from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, roc_auc_score
from sklearn.preprocessing import label_binarize
import numpy as np
import mlflow
import mlflow.sklearn
import matplotlib.pyplot as plt
import seaborn as sns

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
    
    # Логируем метрики в MLFlow
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("f1_score", f1)
    mlflow.log_metric("auc_roc", auc_roc)
    
    # Создаем и сохраняем confusion matrix как артефакт
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix - Logistic Regression')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.savefig('confusion_matrix_lr.png')
    mlflow.log_artifact('confusion_matrix_lr.png')
    plt.close()
    
    print(f"Accuracy: {accuracy}")
    print(f"F1 Score: {f1}")
    print(f"AUC-ROC: {auc_roc}")


if __name__ == "__main__":
    # Настраиваем MLFlow
    mlflow.set_tracking_uri("http://127.0.0.1:8080")
    mlflow.set_experiment("MLOps Lesson 4 - Digits Classification")
    
    with mlflow.start_run(run_name="Logistic Regression"):
        # Логируем параметры конфигурации
        mlflow.log_params(config)
        
        logistic_regression_model = LogisticRegression(
            max_iter=config["logistic_regression"]["max_iter"],
            random_state=config["random_state"]
        )
        
        # Логируем дополнительные параметры модели
        model_params = {
            "model_type": "LogisticRegression",
            "max_iter": config["logistic_regression"]["max_iter"],
            "random_state": config["random_state"],
            "solver": logistic_regression_model.solver,
            "penalty": logistic_regression_model.penalty,
            "C": logistic_regression_model.C
        }
        mlflow.log_params(model_params)

        data = get_data()
        train(logistic_regression_model, data["x_train"], data["y_train"])
        
        # Логируем коэффициенты регрессии после обучения
        coefficients_info = {
            "n_features": logistic_regression_model.coef_.shape[1],
            "n_classes": logistic_regression_model.coef_.shape[0],
            "intercept_shape": logistic_regression_model.intercept_.shape[0]
        }
        mlflow.log_params(coefficients_info)
        
        # Логируем модель
        mlflow.sklearn.log_model(logistic_regression_model, "model")
        
        test(logistic_regression_model, data["x_test"], data["y_test"])
