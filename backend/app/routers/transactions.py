from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.database import get_db, Transaction
from app.middleware.auth import verify_token

router = APIRouter(tags=["Transactions"])

@router.get("/transactions")
def get_transactions(limit: int = 50, db: Session = Depends(get_db)):
    txs = db.query(Transaction).order_by(Transaction.created_at.desc()).limit(limit).all()
    return [
        {
            "id": t.id,
            "amount": t.amount,
            "is_fraud": t.is_fraud,
            "risk_score": t.risk_score,
            "risk_level": t.risk_level,
            "created_at": t.created_at.isoformat()
        } for t in txs
    ]

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(func.count(Transaction.id)).scalar()
    fraud = db.query(func.count(Transaction.id)).filter(Transaction.is_fraud == True).scalar()
    avg_risk = db.query(func.avg(Transaction.risk_score)).scalar()
    return {
        "total_transactions": total or 0,
        "fraud_detected": fraud or 0,
        "fraud_rate_pct": round((fraud / total * 100), 2) if total else 0,
        "average_risk_score": round(avg_risk, 2) if avg_risk else 0
    }
