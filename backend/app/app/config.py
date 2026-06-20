from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    kafka_bootstrap_servers: str
    kafka_topic_raw: str = "sentri.transactions.raw"
    kafka_topic_scored: str = "sentri.transactions.scored"
    kafka_topic_alerts: str = "sentri.alerts.fraud"
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    model_path: str = "./models/"
    env: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()