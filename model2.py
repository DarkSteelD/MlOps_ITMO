from sklearn.tree import DecisionTreeClassifier
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
    
    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("f1_score", f1)
    mlflow.log_metric("auc_roc", auc_roc)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Greens')
    plt.title('Confusion Matrix - Decision Tree')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.savefig('confusion_matrix_dt.png')
    mlflow.log_artifact('confusion_matrix_dt.png')
    plt.close()
    
    print(f"Accuracy: {accuracy}")
    print(f"F1 Score: {f1}")
    print(f"AUC-ROC: {auc_roc}")


if __name__ == "__main__":
    mlflow.set_tracking_uri("http://127.0.0.1:8080")
    mlflow.set_experiment("MLOps Lesson 4 - Digits Classification")
    
    with mlflow.start_run(run_name="Decision Tree"):
        mlflow.log_params(config)
        
        decision_tree_model = DecisionTreeClassifier(
            random_state=config["random_state"],
            max_depth=config["decision_tree"]["max_depth"]
        )
        
        model_params = {
            "model_type": "DecisionTreeClassifier",
            "max_depth": config["decision_tree"]["max_depth"],
            "random_state": config["random_state"],
            "criterion": decision_tree_model.criterion,
            "splitter": decision_tree_model.splitter,
            "min_samples_split": decision_tree_model.min_samples_split,
            "min_samples_leaf": decision_tree_model.min_samples_leaf
        }
        mlflow.log_params(model_params)

        data = get_data()
        train(decision_tree_model, data["x_train"], data["y_train"])
        
        tree_info = {
            "tree_depth": decision_tree_model.tree_.max_depth,
            "n_leaves": decision_tree_model.tree_.n_leaves,
            "n_node_samples": decision_tree_model.tree_.n_node_samples[0],  # корневой узел
            "feature_importances_shape": decision_tree_model.feature_importances_.shape[0],
            "n_features": decision_tree_model.n_features_in_,
            "n_classes": decision_tree_model.n_classes_
        }
        mlflow.log_params(tree_info)
        
        mlflow.sklearn.log_model(decision_tree_model, "model")
        
        test(decision_tree_model, data["x_test"], data["y_test"])
