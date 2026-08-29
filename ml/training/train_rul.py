"""
RUL Baseline Model Training (Section 11.5).
Targeted Mode: Lubrication Circuit & Bearing Wear Degradation Trajectory.
"""

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import numpy as np
import joblib
import os

def train_rul_model():
    X = np.random.normal(loc=1.0, scale=0.2, size=(1000, 13))
    y_rul_hours = np.random.uniform(5.0, 350.0, size=1000)

    X_train, X_test, y_train_rul_hours, y_test_rul_hours = train_test_split(
        X, y_rul_hours, test_size=0.2, random_state=42
    )

    model = GradientBoostingRegressor(random_state=42)
    model.fit(X_train, y_train_rul_hours)

    pred = model.predict(X_test)
    print("MAE:", mean_absolute_error(y_test_rul_hours, pred))

    os.makedirs("ml/models", exist_ok=True)
    joblib.dump(model, "ml/models/rul_model.joblib")
    print("Saved RUL Regressor to ml/models/rul_model.joblib")
    return model

if __name__ == "__main__":
    train_rul_model()
