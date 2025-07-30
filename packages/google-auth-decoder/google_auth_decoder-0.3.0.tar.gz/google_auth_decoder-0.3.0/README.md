# Google Auth data decoder

Utility for decoding Google Auth App's data

## Install and use as utility

```bash
pipx install google_auth_decoder
google_auth_decoder "otpauth-migration://offline?data=CiIKCkCvO217iX16IRkS..."
```

## Install and use as a library

Scan QR code and take the string URL. Then pass it to this utility

```bash
pip install google_auth_decoder
```

```python
import google_auth_decoder
result = google_auth_decoder.decode_url("otpauth-migration://offline?data=CiIKCkCvO217iX16IRkS...")
```

## What is otpauth-migration ?

This is a link from Google Auth App. Scan QR code and take the string URL.

## Developing and testing

```bash
task format
task lint
task type
task test
```

or to run everything

```bash
task check
```

To recompile proto file run

```bash
task compile-proto
```

## Build and publish new version

```bash
uv build
uv publish --token ...
uv run --with google_auth_decoder --no-project -- python -c "import google_auth_decoder; google_auth_decoder.decode_url('foo')"
```


