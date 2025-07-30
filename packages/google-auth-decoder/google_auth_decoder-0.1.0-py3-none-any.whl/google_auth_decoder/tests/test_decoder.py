import pytest

from ..decoder import decode_url
from ..items import Algorithm, DigitCount, OtpParameters, OtpType


@pytest.mark.parametrize(
    "url",
    [
        "",  # Empty string
        "not-a-url",  # No scheme or query
        "otpauth-migration://offline",  # No query params
        "otpauth-migration://offline?data=",  # Empty data param
        "otpauth-migration://offline?foo=bar",  # Wrong param
    ],
)
def test_decode_url_invalid(url: str) -> None:
    with pytest.raises(ValueError, match="No 'data' parameter found in URI."):
        decode_url(url)


def test_decode_url_valid() -> None:
    data = "otpauth-migration://offline?data=ChoKBIWG5pQSBEFsZXgaBkdpdEh1YiABKAEwAgolCg1RSFhIbDhvRU%2BFhuaUEgRBbGV4GghOaW50ZW5kbyABKAEwAhACGAE%3D"
    result = decode_url(data)
    expected_result = [
        OtpParameters(
            secret="QWDONFA",
            name="Alex",
            issuer="GitHub",
            algorithm=Algorithm.SHA1,
            digits=DigitCount.SIX,
            type=OtpType.TOTP,
            counter=0,
            unique_id=None,
        ),
        OtpParameters(
            secret="KFEFQSDMHBXUKT4FQ3TJI",
            name="Alex",
            issuer="Nintendo",
            algorithm=Algorithm.SHA1,
            digits=DigitCount.SIX,
            type=OtpType.TOTP,
            counter=0,
            unique_id=None,
        ),
    ]

    assert result == expected_result
