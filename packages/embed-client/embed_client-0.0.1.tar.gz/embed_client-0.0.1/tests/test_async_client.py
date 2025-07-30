import pytest
import pytest_asyncio
from unittest.mock import patch, MagicMock
from embed_client.async_client import EmbeddingServiceAsyncClient, EmbeddingServiceAPIError, EmbeddingServiceHTTPError, EmbeddingServiceError, EmbeddingServiceConnectionError

BASE_URL = "http://testserver"
PORT = 1234

class MockAiohttpResponse:
    def __init__(self, json_data=None, status=200, raise_http=None, text_data=None):
        self._json = json_data
        self._status = status
        self._raise_http = raise_http
        self._text = text_data
    async def __aenter__(self):
        return self
    async def __aexit__(self, exc_type, exc, tb):
        return None
    async def json(self):
        if self._json is not None:
            return self._json
        raise ValueError("No JSON")
    async def text(self):
        return self._text or ""
    def raise_for_status(self):
        if self._raise_http:
            raise self._raise_http
        return None
    @property
    def status(self):
        return self._status

@pytest_asyncio.fixture
async def client():
    async with EmbeddingServiceAsyncClient(base_url=BASE_URL, port=PORT) as c:
        yield c

def make_url(path):
    return f"{BASE_URL}:{PORT}{path}"

@pytest.mark.asyncio
async def test_health(client):
    with patch.object(client._session, 'get', return_value=MockAiohttpResponse({"status": "ok"})) as mock_get:
        result = await client.health()
        assert result == {"status": "ok"}
        mock_get.assert_called_with(make_url("/health"))

@pytest.mark.asyncio
async def test_get_openapi_schema(client):
    with patch.object(client._session, 'get', return_value=MockAiohttpResponse({"openapi": "3.0.2"})) as mock_get:
        result = await client.get_openapi_schema()
        assert result == {"openapi": "3.0.2"}
        mock_get.assert_called_with(make_url("/openapi.json"))

@pytest.mark.asyncio
async def test_get_commands(client):
    with patch.object(client._session, 'get', return_value=MockAiohttpResponse({"commands": ["embed", "models"]})) as mock_get:
        result = await client.get_commands()
        assert result == {"commands": ["embed", "models"]}
        mock_get.assert_called_with(make_url("/api/commands"))

@pytest.mark.asyncio
async def test_cmd(client):
    with patch.object(client._session, 'post', return_value=MockAiohttpResponse({"result": "ok"})) as mock_post:
        result = await client.cmd("embed", params={"texts": ["abc"]})
        assert result == {"result": "ok"}
        mock_post.assert_called_with(make_url("/cmd"), json={"command": "embed", "params": {"texts": ["abc"]}})

@pytest.mark.asyncio
async def test_init_requires_base_url_and_port():
    with pytest.raises(ValueError):
        EmbeddingServiceAsyncClient(base_url=None, port=PORT)
    with pytest.raises(ValueError):
        EmbeddingServiceAsyncClient(base_url=BASE_URL, port=None)

# Некорректные параметры: не-строка в texts
@pytest.mark.asyncio
async def test_embed_non_string_text(client):
    with patch.object(client._session, 'post', return_value=MockAiohttpResponse({"error": {"code": 422, "message": "Invalid input"}})) as mock_post:
        with pytest.raises(EmbeddingServiceAPIError):
            await client.cmd("embed", params={"texts": [123, "ok"]})

# Некорректные параметры: невалидный params
@pytest.mark.asyncio
async def test_embed_invalid_params_type(client):
    with patch.object(client._session, 'post', return_value=MockAiohttpResponse({"error": {"code": 422, "message": "Invalid params"}})) as mock_post:
        with pytest.raises(EmbeddingServiceAPIError):
            await client.cmd("embed", params="not_a_dict")

# Не-JSON ответ
@pytest.mark.asyncio
async def test_non_json_response(client):
    class BadResponse(MockAiohttpResponse):
        async def json(self):
            raise ValueError("Not a JSON")
    with patch.object(client._session, 'post', return_value=BadResponse(text_data="<html>error</html>")) as mock_post:
        with pytest.raises(EmbeddingServiceError):
            await client.cmd("embed", params={"texts": ["abc"]})

# 500 ошибка сервера
@pytest.mark.asyncio
async def test_server_500_error(client):
    from aiohttp import ClientResponseError
    err = ClientResponseError(request_info=None, history=None, status=500, message="Internal Server Error")
    with patch.object(client._session, 'post', return_value=MockAiohttpResponse(raise_http=err, status=500)) as mock_post:
        with pytest.raises(EmbeddingServiceHTTPError):
            await client.cmd("embed", params={"texts": ["abc"]})

# embed без params
@pytest.mark.asyncio
async def test_embed_no_params(client):
    with patch.object(client._session, 'post', return_value=MockAiohttpResponse({"error": {"code": 422, "message": "Missing params"}})) as mock_post:
        with pytest.raises(EmbeddingServiceAPIError):
            await client.cmd("embed")

# Вектор не той размерности (например, сервер вернул 2D массив, а ожидали 3D)
@pytest.mark.asyncio
async def test_embed_wrong_vector_shape(client):
    # Ожидаем список списков, но сервер вернул список
    with patch.object(client._session, 'post', return_value=MockAiohttpResponse({"embeddings": [1.0, 2.0, 3.0]})) as mock_post:
        result = await client.cmd("embed", params={"texts": ["abc"]})
        vectors = result["embeddings"]
        assert isinstance(vectors, list)
        # Проверяем, что каждый элемент — список (будет False, тест покажет ошибку)
        assert all(isinstance(vec, list) for vec in vectors) is False

# Покрытие: except EmbeddingServiceHTTPError
@pytest.mark.asyncio
async def test_health_http_error(client):
    with patch.object(client._session, 'get', side_effect=EmbeddingServiceHTTPError(500, "fail")):
        with pytest.raises(EmbeddingServiceHTTPError):
            await client.health()

# Покрытие: except EmbeddingServiceConnectionError
@pytest.mark.asyncio
async def test_health_connection_error(client):
    with patch.object(client._session, 'get', side_effect=EmbeddingServiceConnectionError("fail")):
        with pytest.raises(EmbeddingServiceConnectionError):
            await client.health()

# Покрытие: except Exception (ValueError)
@pytest.mark.asyncio
async def test_health_unexpected_error(client):
    with patch.object(client._session, 'get', side_effect=ValueError("fail")):
        with pytest.raises(EmbeddingServiceError):
            await client.health()

# Аналогично для get_openapi_schema
@pytest.mark.asyncio
async def test_get_openapi_schema_http_error(client):
    with patch.object(client._session, 'get', side_effect=EmbeddingServiceHTTPError(500, "fail")):
        with pytest.raises(EmbeddingServiceHTTPError):
            await client.get_openapi_schema()

@pytest.mark.asyncio
async def test_get_openapi_schema_connection_error(client):
    with patch.object(client._session, 'get', side_effect=EmbeddingServiceConnectionError("fail")):
        with pytest.raises(EmbeddingServiceConnectionError):
            await client.get_openapi_schema()

@pytest.mark.asyncio
async def test_get_openapi_schema_unexpected_error(client):
    with patch.object(client._session, 'get', side_effect=ValueError("fail")):
        with pytest.raises(EmbeddingServiceError):
            await client.get_openapi_schema()

# Аналогично для get_commands
@pytest.mark.asyncio
async def test_get_commands_http_error(client):
    with patch.object(client._session, 'get', side_effect=EmbeddingServiceHTTPError(500, "fail")):
        with pytest.raises(EmbeddingServiceHTTPError):
            await client.get_commands()

@pytest.mark.asyncio
async def test_get_commands_connection_error(client):
    with patch.object(client._session, 'get', side_effect=EmbeddingServiceConnectionError("fail")):
        with pytest.raises(EmbeddingServiceConnectionError):
            await client.get_commands()

@pytest.mark.asyncio
async def test_get_commands_unexpected_error(client):
    with patch.object(client._session, 'get', side_effect=ValueError("fail")):
        with pytest.raises(EmbeddingServiceError):
            await client.get_commands()

# Аналогично для cmd
@pytest.mark.asyncio
async def test_cmd_http_error(client):
    with patch.object(client._session, 'post', side_effect=EmbeddingServiceHTTPError(500, "fail")):
        with pytest.raises(EmbeddingServiceHTTPError):
            await client.cmd("embed", params={"texts": ["abc"]})

@pytest.mark.asyncio
async def test_cmd_connection_error(client):
    with patch.object(client._session, 'post', side_effect=EmbeddingServiceConnectionError("fail")):
        with pytest.raises(EmbeddingServiceConnectionError):
            await client.cmd("embed", params={"texts": ["abc"]})

@pytest.mark.asyncio
async def test_cmd_unexpected_error(client):
    with patch.object(client._session, 'post', side_effect=ValueError("fail")):
        with pytest.raises(EmbeddingServiceError):
            await client.cmd("embed", params={"texts": ["abc"]})

# Покрытие: _raise_for_status - ClientResponseError
@pytest.mark.asyncio
async def test_raise_for_status_http_error():
    from aiohttp import ClientResponseError
    client = EmbeddingServiceAsyncClient(base_url=BASE_URL, port=PORT)
    resp = MagicMock()
    resp.raise_for_status.side_effect = ClientResponseError(request_info=None, history=None, status=400, message="fail")
    with pytest.raises(EmbeddingServiceHTTPError):
        await client._raise_for_status(resp)

# Покрытие: _raise_for_status - не ClientResponseError
@pytest.mark.asyncio
async def test_raise_for_status_other_error():
    client = EmbeddingServiceAsyncClient(base_url=BASE_URL, port=PORT)
    resp = MagicMock()
    resp.raise_for_status.side_effect = ValueError("fail")
    with pytest.raises(ValueError):
        await client._raise_for_status(resp)

# Покрытие: __aenter__ и __aexit__ - ошибка при создании/закрытии сессии
@pytest.mark.asyncio
async def test_aenter_aexit_exceptions():
    client = EmbeddingServiceAsyncClient(base_url=BASE_URL, port=PORT)
    # Исключение при создании сессии
    orig = client._session
    client._session = None
    with patch("aiohttp.ClientSession", side_effect=RuntimeError("fail")):
        with pytest.raises(RuntimeError):
            async with client:
                pass
    # Исключение при закрытии сессии
    class BadSession:
        async def close(self):
            raise RuntimeError("fail")
    client._session = BadSession()
    with pytest.raises(RuntimeError):
        await client.__aexit__(None, None, None) 