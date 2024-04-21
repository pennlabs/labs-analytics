import hashlib
from enum import Enum
from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict, json


class CustomModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    def serializable_dict(self, **kwargs):
        default_dict = self.model_dump()
        return jsonable_encoder(default_dict)

    def json(self, **kwargs):
        # Override the json method to customize JSON serialization if needed
        return self.model_dump_json()

    def __str__(self):
        return str(self.json())

    def hash_as_key(self):
        return hashlib.md5(str(self).encode()).hexdigest()[0:16]


class Product(Enum):
    OTHER = 0
    MOBILE_IOS = 1
    MOBILE_ANDROID = 2
    MOBILE_BACKEND = 3
    PORTAL = 4
    PCR = 5
    PDP = 6
    PCA = 7
    PCP = 8
    OHQ = 9
    CLUBS = 10

    def __str__(self):
        return self.name


class RedisEvent(CustomModel):
    key: bytes | str
    value: bytes | str

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
                value=json.dumps(
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
