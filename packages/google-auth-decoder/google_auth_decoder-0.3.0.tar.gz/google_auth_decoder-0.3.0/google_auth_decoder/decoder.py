import base64
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

from google.protobuf import json_format

from . import google_auth_pb2
from .items import OtpParameters


def __decode_protobuf(payload: bytes) -> dict[str, Any]:
    message = google_auth_pb2.MigrationPayload()  # type: ignore[attr-defined]
    message.ParseFromString(payload)
    result: dict[str, Any] = json_format.MessageToDict(message, preserving_proto_field_name=True)
    return result


def decode_url(url: str) -> list[OtpParameters]:
    query = parse_qs(urlparse(url).query)
    data_b64 = query.get("data", [None])[0]

    if not data_b64:
        msg = "No 'data' parameter found in URI."
        raise ValueError(msg)

    decoded = base64.b64decode(unquote(data_b64))
    data = __decode_protobuf(decoded)

    return [OtpParameters.from_dict(entry) for entry in data["otp_parameters"]]
