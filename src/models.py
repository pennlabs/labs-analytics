import hashlib
from enum import Enum

from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from pydantic import BaseModel, ConfigDict, json

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


class Client(BaseModel):
    client_id: str
    secret: str
    product: Product
    disabled: bool = False

    def __init__(self, **data):
        super().__init__(**data)
        self.secret = pwd_context.hash(self.secret)

    def verify_client(self, secret: str, product: Product):
        return pwd_context.verify(secret, self.secret) and product == self.product


class Token(BaseModel):
    access_token: str
    token_type: str
