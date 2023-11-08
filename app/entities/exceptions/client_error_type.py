from enum import Enum


class ClientErrorType(Enum):
    INVALID_INPUT = 1
    UNAUTHORIZED = 2
    FORBIDDEN = 3
    NOT_FOUND = 4
