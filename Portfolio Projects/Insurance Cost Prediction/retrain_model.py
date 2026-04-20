"""
Retrain and save model.pkl using the current Python/sklearn environment.
Run this once to regenerate model.pkl whenever the Python version changes.
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# Load data
df = pd.read_csv("insurance.csv")

# Feature engineering — must match app.py exactly
df["BMI"] = df["Weight"] / ((df["Height"] / 100) ** 2)
df["LogPremiumPrice"] = np.log1p(df["PremiumPrice"])

# Feature selection — same order app.py uses when calling model.predict()
FEATURES = [
    "Age",
    "BMI",
    "NumberOfMajorSurgeries",
    "Diabetes",
    "BloodPressureProblems",
    "AnyChronicDiseases",
    "AnyTransplants",
    "KnownAllergies",
    "HistoryOfCancerInFamily",
]

X = df[FEATURES]
y = df["LogPremiumPrice"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Final model — same config as original notebook
final_model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    min_samples_split=10,
    random_state=42,
)
final_model.fit(X_train, y_train)

from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
y_pred = final_model.predict(X_test)
print(f"R²   : {r2_score(y_test, y_pred):.3f}")
print(f"MAE  : {mean_absolute_error(y_test, y_pred):.3f}")
print(f"RMSE : {mean_squared_error(y_test, y_pred, squared=False):.3f}")

joblib.dump(final_model, "model.pkl")
print("\nmodel.pkl saved successfully.")
