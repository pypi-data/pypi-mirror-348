# PyWaves-Protobuf

[![PyPI version](https://img.shields.io/pypi/v/pywaves-protobuf.svg)](https://pypi.org/project/pywaves-protobuf/)

**Python Protobuf bindings for Waves blockchain.**

## Installation

```bash
pip install pywaves-protobuf
```

## Regenerating Bindings

If schema updates require regenerating Python modules:

  ```bat
generate.bat
```

This will download `protoc` and Waves `.proto` definitions, compile them into the `waves/` package, and perform a verification count.

## License

MIT License — see [LICENSE](LICENSE) for details. 