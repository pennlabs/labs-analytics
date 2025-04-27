import hashlib
import json
from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict


class CustomModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True,)

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

    def __init__(self, **data):
        super().__init__(**data)
        self.key = data["key"]
        self.value = data["value"]


class AnalyticsValue(CustomModel):
    key: str
    value: str
    timestamp: datetime

    def __init__(self, **data):
        super().__init__(**data)
        self.key = data["key"]
        self.value = data["value"]
        self.timestamp = datetime.fromtimestamp(data["timestamp"])


class AnalyticsTxn(CustomModel):
    product: Product
    pennkey: Optional[str] = None
    data: list[AnalyticsValue]

    # init with JSON data
    def __init__(self, **data):
        super().__init__(**data)
        self.product = Product(data["product"])
        self.pennkey = data.get("pennkey")
        self.data = [AnalyticsValue(**value) for value in data["data"]]

    def get_redis_key(self):
        return f"{self.product}.{self.hash_as_key()}"

    def build_redis_data(self) -> list[RedisEvent]:
        return [
            RedisEvent(
                key=f"{self.get_redis_key()}.{value.hash_as_key()}",
                value=json.dumps(
                    {
                        "product": str(self.product),
                        "pennkey": self.pennkey,
                        "timestamp": value.timestamp.timestamp(),
                        "datapoint": value.key,
                        "value": value.value,
                    }
                ),
            )
            for value in self.data
        ]
