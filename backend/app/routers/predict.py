from fastapi import APIRouter, Depends
from app.schemas.transaction import TransactionInput, PredictionOutput, BatchTransactionInput
from app.services.ml_service import ml_service
from app.middleware.auth import verify_token

router = APIRouter(tags=["Prediction"])

@router.post("/predict", response_model=PredictionOutput)
def predict(transaction: TransactionInput, user=Depends(verify_token)):
    result = ml_service.predict(transaction.dict())
    return result

@router.post("/batch-predict")
def batch_predict(batch: BatchTransactionInput, user=Depends(verify_token)):
    results = [ml_service.predict(tx.dict()) for tx in batch.transactions]
    fraud_count = sum(1 for r in results if r["is_fraud"])
    return {
        "total": len(results),
        "fraud_detected": fraud_count,
        "results": results
    }

@router.get("/model/info")
def model_info():
    return {
        "model": "XGBoost + Isolation Forest",
        "features": len(ml_service.feature_names),
        "version": "1.0.0"
    }