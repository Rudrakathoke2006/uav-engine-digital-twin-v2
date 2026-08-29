"""
Evaluates trained ML models and outputs validation metrics.
"""

from sklearn.metrics import classification_report, confusion_matrix, mean_absolute_error
import numpy as np

def evaluate_classifier(y_true, y_pred):
    print("\n--- Fault Classifier Evaluation Report ---")
    print(classification_report(y_true, y_pred))

def evaluate_regressor(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    print(f"\n--- RUL Regressor Evaluation Report ---\nMAE: {mae:.2f} Hours")

if __name__ == "__main__":
    y_true_cls = [0, 1, 2, 3, 0, 1]
    y_pred_cls = [0, 1, 2, 3, 0, 1]
    evaluate_classifier(y_true_cls, y_pred_cls)
