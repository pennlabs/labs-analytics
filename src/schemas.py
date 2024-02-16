from enum import Enum

from pydantic import BaseModel, Field

from models import CustomModel


class Product(str, Enum):
    MOBILE_IOS = "MOBILE_IOS"
    MOBILE_ANDROID = "MOBILE_ANDROID"
    MOBILE_BACKEND = "MOBILE_BACKEND"
    PORTAL = "PORTAL"
    PCR = "PCR"
    PDP = "PDP"
    PCA = "PCA"
    PCP = "PCP"
    OHQ = "OHQ"
    CLUBS = "CLUBS"


# class DataPoints(CustomModel):
