---

## Tech Stack

| Layer | Technology |
|---|---|
| Streaming | Apache Kafka (KRaft mode) |
| ML Models | XGBoost, Isolation Forest, scikit-learn |
| Backend | FastAPI, SQLAlchemy, JWT Auth |
| Frontend | React.js, Recharts |
| Data | 284K+ transactions, SMOTE balancing |
| Testing | pytest (7/7 passing) |

---

## Features

- **Real-time streaming** — transactions flow through Kafka at ~2 tx/sec with sub-50ms scoring
- **ML ensemble** — XGBoost classifier + Isolation Forest anomaly detection trained on 284K transactions with SMOTE class balancing (0.17% fraud rate)
- **REST API** — 7 JWT-secured endpoints with full Swagger docs at `/docs`
- **Live dashboard** — React frontend auto-polling fraud stats, risk scores, and transaction feed every 3 seconds
- **Tested** — 7/7 pytest suite covering auth, prediction, and data endpoints

---

## Quick Start

### Prerequisites
- Python 3.10+
- Java 11+ (for Kafka)
- Node.js 18+

### 1. Clone and install

```bash
git clone https://github.com/vinaydev00/Sentri.git
cd Sentri
pip install -r backend/requirements.txt
```

### 2. Download dataset

Download `creditcard.csv` from [Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) and place it in `ml/data/`.

### 3. Train models

```bash
cd ml
jupyter notebook notebooks/sentri_model_training.ipynb
```

Run all cells — saves models to `ml/models/`.

### 4. Start Kafka

```bash
# Download Apache Kafka 3.7.0, extract to C:\kafka
cd C:\kafka
.\bin\windows\kafka-server-start.bat .\config\kraft\server.properties
```

### 5. Create topics

```bash
.\bin\windows\kafka-topics.bat --create --topic sentri.transactions.raw --bootstrap-server localhost:9092
.\bin\windows\kafka-topics.bat --create --topic sentri.transactions.scored --bootstrap-server localhost:9092
.\bin\windows\kafka-topics.bat --create --topic sentri.alerts.fraud --bootstrap-server localhost:9092
```

### 6. Start everything

```bash
# Terminal 1 - Backend
cd backend && uvicorn app.main:app --reload

# Terminal 2 - Consumer (scoring engine)
python kafka/consumer.py

# Terminal 3 - Producer (transaction simulator)
python kafka/producer.py

# Terminal 4 - Dashboard
cd dashboard && npm install && npm run dev
```

Open `http://localhost:5173` for the dashboard and `http://localhost:8000/docs` for the API.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/token` | Get JWT token |
| POST | `/predict` | Score a single transaction |
| POST | `/batch-predict` | Score multiple transactions |
| GET | `/model/info` | Model metadata |
| GET | `/stats` | Fraud detection statistics |
| GET | `/transactions` | Recent scored transactions |
| GET | `/health` | Service health check |

---

## ML Pipeline

- **Dataset**: Kaggle Credit Card Fraud (284,807 transactions, 492 fraud cases)
- **Class imbalance**: Handled with SMOTE oversampling
- **Models**: XGBoost (classification) + Isolation Forest (anomaly scoring)
- **Evaluation**: Confusion matrix, Precision/Recall, F1, ROC-AUC

---

*Built by [Vinay](https://github.com/vinaydev00)*
