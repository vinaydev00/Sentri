import json
import time
import random
import uuid
from confluent_kafka import Producer

conf = {"bootstrap.servers": "localhost:9092"}
producer = Producer(conf)

TOPIC = "sentri.transactions.raw"

def generate_fake_transaction():
    transaction = {
        "transaction_id": str(uuid.uuid4()),
        "Time": random.uniform(0, 172792),
        "Amount": round(random.uniform(1, 5000), 2),
    }
    for i in range(1, 29):
        transaction[f"V{i}"] = round(random.gauss(0, 1.5), 4)

    if random.random() < 0.05:
        transaction["V1"] = round(random.uniform(-20, -10), 4)
        transaction["V4"] = round(random.uniform(8, 15), 4)
        transaction["Amount"] = round(random.uniform(2000, 9000), 2)

    return transaction

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")

def main():
    print(f"Sentri producer streaming to topic {TOPIC}... Ctrl+C to stop")
    count = 0
    try:
        while True:
            tx = generate_fake_transaction()
            producer.produce(
                TOPIC,
                key=tx["transaction_id"],
                value=json.dumps(tx),
                callback=delivery_report
            )
            producer.poll(0)
            count += 1
            if count % 10 == 0:
                print(f"   ...{count} transactions sent")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print(f"Stopped. Total sent: {count}")
    finally:
        producer.flush()

if __name__ == "__main__":
    main()
