import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import (
    confusion_matrix,
    roc_curve,
    auc,
    precision_recall_curve,
    classification_report,
)


def plot_confusion_matrix(
    y_true, y_pred, labels=None, title="Confusion Matrix", save_path=None
):
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    plt.figure(figsize=(6, 5))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels
    )
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title(title)
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path)
    plt.close()


def plot_roc_curve(y_true, y_score, title="ROC Curve", save_path=None):
    fpr, tpr, _ = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)
    plt.figure(figsize=(6, 5))
    plt.plot(
        fpr, tpr, color="darkorange", lw=2, label=f"ROC curve (area = {roc_auc:.2f})"
    )
    plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(title)
    plt.legend(loc="lower right")
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path)
    plt.close()


def plot_precision_recall_curve(
    y_true, y_score, title="Precision-Recall Curve", save_path=None
):
    precision, recall, _ = precision_recall_curve(y_true, y_score)
    plt.figure(figsize=(6, 5))
    plt.plot(recall, precision, color="blue", lw=2)
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title(title)
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path)
    plt.close()


def print_classification_report(y_true, y_pred):
    print(classification_report(y_true, y_pred, digits=4))


def plot_feature_importance(
    importances,
    feature_names,
    filename="models/feature_importance.png",
    top_n=10,
    title="Top Feature Importances",
):
    # Convert to arrays for sorting
    importances = np.array(importances)
    feature_names = np.array(feature_names)
    # Sort and select top_n
    indices = np.argsort(importances)[-top_n:][::-1]
    plt.figure(figsize=(8, max(4, top_n * 0.5)))
    plt.barh(range(top_n), importances[indices][::-1], align="center")
    plt.yticks(range(top_n), feature_names[indices][::-1])
    plt.xlabel("Importance")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
