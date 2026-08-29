"""
Fault Classifier Training (Section 11.4).
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
import joblib
import os

def train_fault_classifier():
    X = np.random.normal(loc=1.0, scale=0.2, size=(1200, 13))
    y = np.random.choice([
        "normal",
        "lubrication_degradation",
        "overheating",
        "injector_fault",
        "abnormal_vibration"
    ], size=1200)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=300,
        class_weight="balanced",
        random_state=42
    )
    model.fit(X_train, y_train)

    print("\n--- Classification Report ---")
    print(classification_report(y_test, model.predict(X_test)))
    print("\n--- Confusion Matrix ---")
    print(confusion_matrix(y_test, model.predict(X_test)))

    os.makedirs("ml/models", exist_ok=True)
    joblib.dump(model, "ml/models/fault_model.joblib")
    print("\nSaved Fault Classifier to ml/models/fault_model.joblib")
    return model

if __name__ == "__main__":
    train_fault_classifier()
