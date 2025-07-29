# deepjson-py-connector

**A Python connector for interacting with DeepJSON, a flexible JSON document server for storage, scripting, and automation.**

---

## Features

- 🔐 Login with username/password and manage JWT tokens
- 📦 GET, POST, PUT, DELETE operations for keys
- 🖼️ Upload and move binary files (PDFs, images, etc.)
- 🧠 Scriptable value embedding using DeepJSON logic
- ⚙️ Works in sync mode with any DeepJSON backend
- ✅ Lightweight and dependency-friendly

---

## Installation

```bash
pip install deepjson-py-connector
```

---

## Usage

```python
from deepjson_py_connector import DeepJSONConnector

client = DeepJSONConnector({
    "base_url": "http://localhost:3000",
    "token": "your-jwt-token"
})

# GET example
response = client.get("my-key")

# POST a JSON string
client.post("my-key", '{"name": "John"}')

# Upload a file
with open("receipt.pdf", "rb") as f:
    client.upload_file("receipts/july", f)
```

---

## Flags & Options

Set optional flags before a request:

```python
client.set_binary(True)           # If you want binary content
client.set_get_body(True)         # GET with body override
client.set_overwrite_key(True)    # POST can overwrite if enabled
```

All flags reset automatically after each request.

---

## Testing

Tests are written with `pytest`.

```bash
pytest
```

---

## Project Structure

```
deepjson_py_connector/
├── __init__.py
├── client.py      # Main connector logic
├── tests/
│   └── test_client.py
└── pyproject.toml
```

---

## License

MIT © 2025 Eren Havuc