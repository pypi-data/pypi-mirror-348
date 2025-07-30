# visualizer.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from sklearn.metrics import roc_curve, auc, precision_recall_curve, average_precision_score
import numpy as np

def plot_class_distribution(y_true, output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)
    plt.figure(figsize=(8, 4))
    sns.countplot(x=y_true)
    plt.title("Class Distribution")
    plt.xlabel("Class")
    plt.ylabel("Count")
    plt.tight_layout()
    path = os.path.join(output_dir, "class_distribution.png")
    plt.savefig(path)
    plt.close()
    return path

def plot_confusion_matrix(cm, labels, output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=labels, yticklabels=labels, cmap="Blues")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.title("Confusion Matrix")
    path = os.path.join(output_dir, "confusion_matrix.png")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
    return path

def plot_error_distribution(y_true, y_pred, output_dir="outputs"):
    os.makedirs(output_dir, exist_ok=True)
    errors = y_true - y_pred
    plt.figure(figsize=(8, 4))
    sns.histplot(errors, kde=True)
    plt.title("Error Distribution")
    plt.xlabel("Error")
    plt.tight_layout()
    path = os.path.join(output_dir, "error_distribution.png")
    plt.savefig(path)
    plt.close()
    return path


def plot_roc_curve(y_true, y_prob, output_dir="outputs"):
    """
    Plots ROC Curve.
    y_true: true binary or multiclass labels
    y_prob: predicted probabilities (pd.Series for binary, pd.DataFrame for multiclass)
    """
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(7, 6))

    if isinstance(y_prob, pd.Series) or (isinstance(y_prob, np.ndarray) and y_prob.ndim == 1):
        # Binary classification ROC
        fpr, tpr, _ = roc_curve(y_true, y_prob)
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    else:
        # Multiclass ROC: one vs rest
        classes = y_prob.columns if isinstance(y_prob, pd.DataFrame) else range(y_prob.shape[1])
        for i, class_label in enumerate(classes):
            y_true_bin = (y_true == class_label).astype(int)
            y_prob_class = y_prob[class_label] if isinstance(y_prob, pd.DataFrame) else y_prob[:, i]
            fpr, tpr, _ = roc_curve(y_true_bin, y_prob_class)
            roc_auc = auc(fpr, tpr)
            plt.plot(fpr, tpr, lw=2, label=f'Class {class_label} (area = {roc_auc:.2f})')

    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.tight_layout()

    path = os.path.join(output_dir, "roc_curve.png")
    plt.savefig(path)
    plt.close()
    return path


def plot_precision_recall_curve(y_true, y_prob, output_dir="outputs"):
    """
    Plots Precision-Recall Curve.
    y_true: true binary or multiclass labels
    y_prob: predicted probabilities (pd.Series for binary, pd.DataFrame for multiclass)
    """
    os.makedirs(output_dir, exist_ok=True)

    plt.figure(figsize=(7, 6))

    if isinstance(y_prob, pd.Series) or (isinstance(y_prob, np.ndarray) and y_prob.ndim == 1):
        # Binary classification PR curve
        precision, recall, _ = precision_recall_curve(y_true, y_prob)
        ap = average_precision_score(y_true, y_prob)
        plt.plot(recall, precision, color='b', lw=2, label=f'AP = {ap:.2f}')
    else:
        # Multiclass PR curve (one vs rest)
        classes = y_prob.columns if isinstance(y_prob, pd.DataFrame) else range(y_prob.shape[1])
        for i, class_label in enumerate(classes):
            y_true_bin = (y_true == class_label).astype(int)
            y_prob_class = y_prob[class_label] if isinstance(y_prob, pd.DataFrame) else y_prob[:, i]
            precision, recall, _ = precision_recall_curve(y_true_bin, y_prob_class)
            ap = average_precision_score(y_true_bin, y_prob_class)
            plt.plot(recall, precision, lw=2, label=f'Class {class_label} AP = {ap:.2f}')

    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.legend(loc="lower left")
    plt.tight_layout()

    path = os.path.join(output_dir, "precision_recall_curve.png")
    plt.savefig(path)
    plt.close()
    return path
