import joblib
import numpy as np
import pandas as pd
from pathlib import Path

MODEL_DIR = Path(__file__).parent.parent.parent.parent / "ml" / "models"

class MLService:
    def __init__(self):
        self.xgb_model = joblib.load(MODEL_DIR / "xgb_model.pkl")
        self.iso_forest = joblib.load(MODEL_DIR / "isolation_forest.pkl")
        self.scaler = joblib.load(MODEL_DIR / "scaler.pkl")
        self.feature_names = joblib.load(MODEL_DIR / "feature_names.pkl")

    def predict(self, transaction: dict) -> dict:
        df = pd.DataFrame([transaction])

        amount_mean = self.scaler.mean_[0]
        amount_scale = self.scaler.scale_[0]

        if "Amount" in df.columns:
            df["Amount_Scaled"] = (df["Amount"] - amount_mean) / amount_scale
            df = df.drop("Amount", axis=1)
        if "Time" in df.columns:
            df["Time_Scaled"] = (df["Time"] - amount_mean) / amount_scale
            df = df.drop("Time", axis=1)

        df = df.reindex(columns=self.feature_names, fill_value=0)

        fraud_proba = float(self.xgb_model.predict_proba(df)[0][1])
        fraud_pred = int(self.xgb_model.predict(df)[0])
        anomaly_score = float(self.iso_forest.score_samples(df)[0])

        risk_score = round(fraud_proba * 100, 2)

        if risk_score >= 80:
            risk_level = "high"
        elif risk_score >= 40:
            risk_level = "medium"
        else:
            risk_level = "low"

        return {
            "is_fraud": bool(fraud_pred),
            "fraud_probability": fraud_proba,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "anomaly_score": anomaly_score
        }

ml_service = MLService()
