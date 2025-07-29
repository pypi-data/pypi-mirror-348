from dataclasses import dataclass, field

from .errors import ErrorCode


@dataclass(frozen=True)
class MessageBase:
    """
    Base class for messages
    """

    identifier: str = ""


@dataclass(frozen=True)
class Request(MessageBase):
    """
    Request message
    """


@dataclass(frozen=True)
class ReadRequest(Request):
    """
    Read request message
    """


@dataclass(frozen=True)
class WriteRequest(Request):
    """
    Write request message
    """

    data: int = 0


@dataclass(frozen=True)
class SaveRequest(Request):
    """
    Save request message
    """


@dataclass(frozen=True)
class Response(MessageBase):
    """
    Response message
    """

    data: bytes = field(default_factory=bytes)
    error_code: ErrorCode = ErrorCode.NO_ERROR

    def has_error(self) -> bool:
        return self.error_code != ErrorCode.NO_ERROR
