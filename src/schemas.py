from datetime import datetime
from typing import Optional

from src.models import CustomModel, Product, RedisEvent


class AuthRequest:
    client_id: str
    secret: str
    product: Product = Product.OTHER


class AnalyticsTxn(CustomModel):
    product: Product
    pennkey: Optional[str] = None
    timestamp: datetime
    data: list[RedisEvent]

    # init with JSON data
    def __init__(self, **data):
        super().__init__(**data)
        self.timestamp = datetime.fromtimestamp(data["timestamp"])
        self.data = [RedisEvent(**event) for event in data["data"]]
        self.product = Product(data["product"])
        self.pennkey = data.get("pennkey")

    def get_redis_key(self):
        return f"{self.product}.{self.hash_as_key()}"

    def build_redis_data(self) -> list[RedisEvent]:
        return [
            RedisEvent(
                key=f"{self.get_redis_key()}.{event.hash_as_key()}",
                value=str(
                    {
                        "product": str(self.product),
                        "pennkey": self.pennkey,
                        "timestamp": self.timestamp.timestamp(),
                        "datapoint": event.key,
                        "value": event.value,
                    }
                ),
            )
            for event in self.data
        ]
