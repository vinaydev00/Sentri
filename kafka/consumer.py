import json
import sys
import os
import uuid
from confluent_kafka import Consumer, Producer

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))
from app.services.ml_service import ml_service
from app.models.database import SessionLocal, Transaction

conf = {
    "bootstrap.servers": "localhost:9092",
    "group.id": "sentri-scoring-engine",
    "auto.offset.reset": "earliest"
}

consumer = Consumer(conf)
producer = Producer({"bootstrap.servers": "localhost:9092"})

RAW_TOPIC = "sentri.transactions.raw"
SCORED_TOPIC = "sentri.transactions.scored"
ALERT_TOPIC = "sentri.alerts.fraud"

def main():
    consumer.subscribe([RAW_TOPIC])
    print(f"Sentri scoring engine listening on {RAW_TOPIC}... Ctrl+C to stop")

    processed = 0
    fraud_count = 0
    db = SessionLocal()

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            tx = json.loads(msg.value().decode("utf-8"))
            tx_id = tx.pop("transaction_id")

            result = ml_service.predict(tx)
            result["transaction_id"] = tx_id
            result["amount"] = tx["Amount"]

            producer.produce(SCORED_TOPIC, value=json.dumps(result))

            db_tx = Transaction(
                id=tx_id,
                amount=tx["Amount"],
                is_fraud=result["is_fraud"],
                fraud_probability=result["fraud_probability"],
                risk_score=result["risk_score"],
                risk_level=result["risk_level"],
                anomaly_score=result["anomaly_score"]
            )
            db.add(db_tx)
            db.commit()

            if result["is_fraud"]:
                fraud_count += 1
                producer.produce(ALERT_TOPIC, value=json.dumps(result))
                print(f"FRAUD ALERT | {tx_id[:8]} | ${tx['Amount']:.2f} | risk={result['risk_score']}%")
            else:
                print(f"OK | {tx_id[:8]} | ${tx['Amount']:.2f} | risk={result['risk_score']}%")

            processed += 1
            producer.poll(0)

            if processed % 20 == 0:
                print(f"   --- Processed: {processed} | Fraud flagged: {fraud_count} ---")

    except KeyboardInterrupt:
        print(f"Stopped. Processed: {processed}, Fraud: {fraud_count}")
    finally:
        producer.flush()
        consumer.close()
        db.close()

if __name__ == "__main__":
    main()
