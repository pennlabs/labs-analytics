import hashlib

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict


class CustomModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    def serializable_dict(self, **kwargs):
        default_dict = self.model_dump()
        return jsonable_encoder(default_dict)

    def __str__(self):
        return str(self.serializable_dict())

    def hash_as_key(self):
        return hashlib.md5(str(self).encode()).hexdigest()[0:16]
