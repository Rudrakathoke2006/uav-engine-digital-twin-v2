"""
Anomaly Model Training (Section 11.3).
"""

from sklearn.ensemble import IsolationForest
import numpy as np
import joblib
import os

def train_anomaly_model():
    X_normal = np.random.normal(loc=1.0, scale=0.05, size=(1000, 13))

    model = IsolationForest(
        n_estimators=250,
        contamination=0.02,
        random_state=42
    )
    model.fit(X_normal)
    os.makedirs("ml/models", exist_ok=True)
    joblib.dump(model, "ml/models/anomaly_model.joblib")
    print("Saved Isolation Forest model to ml/models/anomaly_model.joblib")
    return model

if __name__ == "__main__":
    train_anomaly_model()
