from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, roc_auc_score
from sklearn.preprocessing import label_binarize
import numpy as np
import wandb

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
    
    # Логируем метрики в WandB
    wandb.log({
        "accuracy": accuracy,
        "f1_score": f1,
        "auc_roc": auc_roc,
        "confusion_matrix": wandb.plot.confusion_matrix(
            probs=None,
            y_true=y_test,
            preds=y_pred,
            class_names=[str(i) for i in range(10)]
        )
    })
    
    print(f"Accuracy: {accuracy}")
    print(f"F1 Score: {f1}")
    print(f"AUC-ROC: {auc_roc}")


if __name__ == "__main__":
    # Инициализируем WandB
    wandb.init(
        project="mlops-lesson-4",
        name="logistic-regression-digits",
        config=config
    )
    
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
    wandb.config.update(model_params)

    data = get_data()
    train(logistic_regression_model, data["x_train"], data["y_train"])
    
    # Логируем коэффициенты регрессии после обучения
    coefficients_info = {
        "n_features": logistic_regression_model.coef_.shape[1],
        "n_classes": logistic_regression_model.coef_.shape[0],
        "intercept_shape": logistic_regression_model.intercept_.shape[0]
    }
    wandb.config.update(coefficients_info)
    
    test(logistic_regression_model, data["x_test"], data["y_test"])
    
    # Завершаем WandB run
    wandb.finish()
