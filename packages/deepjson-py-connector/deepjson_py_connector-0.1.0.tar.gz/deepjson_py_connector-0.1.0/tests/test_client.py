import pytest
from io import BytesIO
from deepjson_py_connector import DeepJSONConnector

BASE_URL = "http://localhost:3000"

def test_token_setter():
    client = DeepJSONConnector({"base_url": BASE_URL})
    client.token = "abc123"
    assert client.get_token() == "abc123"

def test_set_flags():
    client = DeepJSONConnector({"base_url": BASE_URL})
    client.set_binary(True).set_overwrite_key(True).set_get_body(True)
    assert client.binary is True
    assert client.overwrite_key is True
    assert client.get_body is True

def test_reset_flags_after_request(monkeypatch):
    client = DeepJSONConnector({"base_url": BASE_URL})
    client.token = "dummy"

    # Mock the session.request to avoid real HTTP call
    def mock_request(method, url, **kwargs):
        class DummyResponse:
            def raise_for_status(self): pass
            def json(self): return {"status": "ok"}
            content = b'binary-data'
        return DummyResponse()

    monkeypatch.setattr(client.session, "request", mock_request)

    # Trigger a GET request and test internal state resets
    client.set_binary(True).set_get_body(True)
    result = client.get("test-key", "dummy-value")
    assert result == b'binary-data'
    assert client.binary is False
    assert client.get_body is False

def test_error_handling(monkeypatch):
    client = DeepJSONConnector({"base_url": BASE_URL})
    
    def bad_request(method, url, **kwargs):
        raise Exception("Mock error")

    monkeypatch.setattr(client.session, "request", bad_request)

    with pytest.raises(Exception) as exc:
        client.get("test-key")

    assert "Mock error" in str(exc.value)

def test_post(monkeypatch):
    client = DeepJSONConnector({"base_url": BASE_URL})
    client.token = "dummy"

    def mock_request(method, url, **kwargs):
        class DummyResponse:
            def raise_for_status(self): pass
            def json(self): return {"status": "posted"}
        return DummyResponse()

    monkeypatch.setattr(client.session, "request", mock_request)
    result = client.post("test-key", "value")
    assert result == {"status": "posted"}

def test_put(monkeypatch):
    client = DeepJSONConnector({"base_url": BASE_URL})
    client.token = "dummy"

    def mock_request(method, url, **kwargs):
        class DummyResponse:
            def raise_for_status(self): pass
            def json(self): return {"updated": True}
        return DummyResponse()

    monkeypatch.setattr(client.session, "request", mock_request)
    result = client.put("test-key", "value")
    assert result == {"updated": True}

def test_delete(monkeypatch):
    client = DeepJSONConnector({"base_url": BASE_URL})
    client.token = "dummy"

    def mock_request(method, url, **kwargs):
        class DummyResponse:
            def raise_for_status(self): pass
            def json(self): return {"deleted": True}
        return DummyResponse()

    monkeypatch.setattr(client.session, "request", mock_request)
    result = client.delete("test-key")
    assert result == {"deleted": True}

def test_upload_file(monkeypatch):
    client = DeepJSONConnector({"base_url": BASE_URL})
    client.token = "dummy"

    class DummyFile(BytesIO):
        name = "dummy.txt"
        def __init__(self):
            super().__init__(b"mock file content")
        def stream(self): return self

    def mock_request(method, url, **kwargs):
        class DummyResponse:
            def raise_for_status(self): pass
            def json(self): return {"upload": "success"}
        return DummyResponse()

    monkeypatch.setattr(client.session, "request", mock_request)
    result = client.upload_file("test-key", DummyFile())
    assert result == {"upload": "success"}