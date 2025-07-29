from enum import Enum


class AbstractPropertyLogicalType(str, Enum):
    DATE = "date"
    INTEGER = "integer"
    STRING = "string"

    def __str__(self) -> str:
        return str(self.value)
