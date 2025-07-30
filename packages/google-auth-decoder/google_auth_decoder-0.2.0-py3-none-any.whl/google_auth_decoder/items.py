import base64
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Self


class Algorithm(StrEnum):
    ALGORITHM_UNSPECIFIED = "ALGORITHM_UNSPECIFIED"
    SHA1 = "SHA1"
    SHA256 = "SHA256"
    SHA512 = "SHA512"
    MD5 = "MD5"


class DigitCount(StrEnum):
    DIGIT_COUNT_UNSPECIFIED = "DIGIT_COUNT_UNSPECIFIED"
    SIX = "SIX"
    EIGHT = "EIGHT"
    SEVEN = "SEVEN"


class OtpType(StrEnum):
    OTP_TYPE_UNSPECIFIED = "OTP_TYPE_UNSPECIFIED"
    HOTP = "HOTP"
    TOTP = "TOTP"


@dataclass
class OtpParameters:
    secret: str
    name: str | None
    issuer: str | None
    algorithm: Algorithm
    digits: DigitCount
    type: OtpType
    counter: int | None = 0
    unique_id: str | None = None

    @classmethod
    def from_dict(cls, param: dict[str, Any]) -> Self:
        return cls(
            secret=cls.base64_to_base32(param.get("secret", "")),
            name=param.get("name"),
            issuer=param.get("issuer"),
            algorithm=Algorithm(param["algorithm"]),
            digits=DigitCount(param["digits"]),
            type=OtpType(param["type"]),
            counter=int(param.get("counter", 0)),
            unique_id=param.get("uniqueId"),
        )

    @staticmethod
    def base64_to_base32(base64_str: str) -> str:
        raw_bytes = base64.b64decode(base64_str)
        return base64.b32encode(raw_bytes).decode("utf-8").replace("=", "")

    def __str__(self) -> str:
        return (
            f"Issuer: {self.issuer}\n"
            f"Name: {self.name}\n"
            f"Secret: {self.secret}\n"
            f"Algorithm: {self.algorithm}\n"
            f"Digits: {self.digits}\n"
            f"Type: {self.type}\n"
            f"Counter: {self.counter}\n"
            f"Unique ID: {self.unique_id}\n"
        )
