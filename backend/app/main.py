from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, predict, transactions

app = FastAPI(
    title="Sentri",
    description="Real-time fraud detection engine - Kafka + ML + FastAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(predict.router)
app.include_router(transactions.router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "Sentri", "version": "1.0.0"}
