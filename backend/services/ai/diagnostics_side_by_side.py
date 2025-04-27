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

def plot_confusion_matrix_side_by_side(y_true_train, y_pred_train, y_true_cv, y_pred_cv, labels=None, save_path=None):
    cm_train = confusion_matrix(y_true_train, y_pred_train, labels=labels)
    cm_cv = confusion_matrix(y_true_cv, y_pred_cv, labels=labels)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    sns.heatmap(cm_train, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels, ax=axes[0])
    axes[0].set_title("Confusion Matrix (Training Data)")
    axes[0].set_xlabel("Predicted")
    axes[0].set_ylabel("Actual")
    sns.heatmap(cm_cv, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels, ax=axes[1])
    axes[1].set_title("Confusion Matrix (Cross-Validation)")
    axes[1].set_xlabel("Predicted")
    axes[1].set_ylabel("")
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path)
    plt.close()

def plot_roc_curve_side_by_side(y_true_train, y_score_train, y_true_cv, y_score_cv, save_path=None):
    fpr_train, tpr_train, _ = roc_curve(y_true_train, y_score_train)
    roc_auc_train = auc(fpr_train, tpr_train)
    fpr_cv, tpr_cv, _ = roc_curve(y_true_cv, y_score_cv)
    roc_auc_cv = auc(fpr_cv, tpr_cv)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(fpr_train, tpr_train, color="darkorange", lw=2, label=f"AUC = {roc_auc_train:.2f}")
    axes[0].plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
    axes[0].set_xlim([0.0, 1.0])
    axes[0].set_ylim([0.0, 1.05])
    axes[0].set_xlabel("False Positive Rate")
    axes[0].set_ylabel("True Positive Rate")
    axes[0].set_title("ROC Curve (Training Data)")
    axes[0].legend(loc="lower right")
    axes[1].plot(fpr_cv, tpr_cv, color="darkorange", lw=2, label=f"AUC = {roc_auc_cv:.2f}")
    axes[1].plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
    axes[1].set_xlim([0.0, 1.0])
    axes[1].set_ylim([0.0, 1.05])
    axes[1].set_xlabel("False Positive Rate")
    axes[1].set_ylabel("")
    axes[1].set_title("ROC Curve (Cross-Validation)")
    axes[1].legend(loc="lower right")
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path)
    plt.close()

def plot_precision_recall_curve_side_by_side(y_true_train, y_score_train, y_true_cv, y_score_cv, save_path=None):
    precision_train, recall_train, _ = precision_recall_curve(y_true_train, y_score_train)
    precision_cv, recall_cv, _ = precision_recall_curve(y_true_cv, y_score_cv)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    axes[0].plot(recall_train, precision_train, color="blue", lw=2)
    axes[0].set_xlabel("Recall")
    axes[0].set_ylabel("Precision")
    axes[0].set_title("Precision-Recall Curve (Training Data)")
    axes[1].plot(recall_cv, precision_cv, color="blue", lw=2)
    axes[1].set_xlabel("Recall")
    axes[1].set_ylabel("")
    axes[1].set_title("Precision-Recall Curve (Cross-Validation)")
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path)
    plt.close()
