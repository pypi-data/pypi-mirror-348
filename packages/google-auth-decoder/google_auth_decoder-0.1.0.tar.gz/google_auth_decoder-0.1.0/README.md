# Google Auth data decoder

Utility for decoding Google Auth App's data

## How to use

Scan QR code and take the string URL. Then pass it to this utility

```bash
uv run google_auth_decoder "otpauth-migration://offline?data=CiIKCkCvO217iX16IRkS..."
```

or 
```bash
task run -- "otpauth-migration://offline?data=CiIKCkCvO217iX16IRkS..."
```

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
