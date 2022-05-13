from enum import Enum

class RecoveryMethodEnum(Enum):
    WATERFLOOD = 1
    FRACTURING = 2
    GASINJECTION = 3
    CO2FLOOD = 4

class CompletionMethodsEnum(Enum):
    OPENHOLE = 1
    CASED = 2
    ACIDWASH = 3
    MESH = 4
