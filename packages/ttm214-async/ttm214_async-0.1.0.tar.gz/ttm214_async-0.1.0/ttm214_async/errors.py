from enum import Enum


class ErrorCode(Enum):
    """
    Error enumeration
    """

    NO_ERROR = 0x00
    INTRUMENT_FAILURE = 0x30
    NUMERICAL_VALUE_OUT_OF_RANGE = 0x31
    NO_DATA_AVAILABLE = 0x32
    UNVALID_ASCII_CODE = 0x33
    FORMAT_ERROR = 0x34
    BCC_ERROR = 0x35
    OVERRUN_ERROR = 0x36
    FRAMING_ERROR = 0x37
    PARITY_ERROR = 0x38
    AT_ERROR = 0x39

    ILLEGAL_RESPONSE_LENGTH = 0x40
    ILLEGAL_RESPONSE_CODE = 0x41
    TIMEOUT = 0x42
