# evaluator.py
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    mean_absolute_error, mean_squared_error, r2_score
)
from sklearn.utils.multiclass import type_of_target

def evaluate_classification(y_true, y_pred, average='macro'):
    """
    Evaluate classification metrics.
    """
    return {
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(y_true, y_pred, average=average, zero_division=0),
        "Recall": recall_score(y_true, y_pred, average=average, zero_division=0),
        "F1 Score": f1_score(y_true, y_pred, average=average, zero_division=0),
    }

def evaluate_multilabel_classification(y_true, y_pred):
    """
    Evaluate multilabel classification metrics using 'samples' averaging.
    """
    return evaluate_classification(y_true, y_pred, average='samples')

def evaluate_regression(y_true, y_pred):
    """
    Evaluate regression metrics.
    """
    return {
        "MAE": mean_absolute_error(y_true, y_pred),
        "MSE": mean_squared_error(y_true, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
        "R2 Score": r2_score(y_true, y_pred),
    }

def get_task_type(y_true):
    """
    Detect task type based on y_true.
    Returns one of 'classification', 'multilabel', 'regression'.
    """
    # Convert to numpy array if list
    y_true = np.array(y_true)
    target_type = type_of_target(y_true)

    if target_type == "multilabel-indicator":
        return "multilabel"
    elif target_type in ["continuous", "continuous-multioutput"]:
        return "regression"
    else:
        return "classification"

def evaluate(y_true, y_pred):
    """
    Evaluate y_pred against y_true based on detected task type.
    """
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    task_type = get_task_type(y_true)

    if task_type == "classification":
        return evaluate_classification(y_true, y_pred)
    elif task_type == "multilabel":
        return evaluate_multilabel_classification(y_true, y_pred)
    elif task_type == "regression":
        return evaluate_regression(y_true, y_pred)
    else:
        raise ValueError(f"Unknown task type detected: {task_type}")
