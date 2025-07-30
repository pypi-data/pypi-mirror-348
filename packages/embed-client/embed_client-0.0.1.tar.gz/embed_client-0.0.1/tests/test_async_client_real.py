import pytest
import pytest_asyncio
from embed_client.async_client import EmbeddingServiceAsyncClient, EmbeddingServiceAPIError, EmbeddingServiceHTTPError

BASE_URL = "http://localhost"
PORT = 8001

async def is_service_available():
    try:
        async with EmbeddingServiceAsyncClient(base_url=BASE_URL, port=PORT) as client:
            await client.health()
        return True
    except Exception:
        return False

@pytest_asyncio.fixture
async def real_client():
    async with EmbeddingServiceAsyncClient(base_url=BASE_URL, port=PORT) as client:
        yield client

@pytest.mark.asyncio
@pytest.mark.integration
async def test_real_health(real_client):
    if not await is_service_available():
        pytest.skip("Real service on localhost:8001 is not available.")
    result = await real_client.health()
    assert "status" in result
    assert result["status"] in ("ok", "error")

@pytest.mark.asyncio
@pytest.mark.integration
async def test_real_openapi(real_client):
    if not await is_service_available():
        pytest.skip("Real service on localhost:8001 is not available.")
    result = await real_client.get_openapi_schema()
    assert "openapi" in result
    assert result["openapi"].startswith("3.")

@pytest.mark.asyncio
@pytest.mark.integration
async def test_real_get_commands(real_client):
    if not await is_service_available():
        pytest.skip("Real service on localhost:8001 is not available.")
    result = await real_client.get_commands()
    assert isinstance(result, dict)

@pytest.mark.asyncio
@pytest.mark.integration
async def test_real_cmd_help(real_client):
    if not await is_service_available():
        pytest.skip("Real service on localhost:8001 is not available.")
    result = await real_client.cmd("help")
    assert isinstance(result, dict)

def extract_vectors(result):
    if "embeddings" in result:
        return result["embeddings"]
    elif "result" in result:
        if isinstance(result["result"], list):
            return result["result"]
        elif isinstance(result["result"], dict) and "embeddings" in result["result"]:
            return result["result"]["embeddings"]
        else:
            pytest.fail("No embeddings in result['result']")
    else:
        pytest.fail("No embeddings or result in response")

@pytest.mark.asyncio
@pytest.mark.integration
async def test_real_embed_vector(real_client):
    if not await is_service_available():
        pytest.skip("Real service on localhost:8001 is not available.")
    texts = ["hello world", "test embedding"]
    params = {"texts": texts}
    result = await real_client.cmd("embed", params=params)
    vectors = extract_vectors(result)
    assert isinstance(vectors, list)
    assert len(vectors) == len(texts)
    assert all(isinstance(vec, list) for vec in vectors)
    assert all(isinstance(x, (float, int)) for vec in vectors for x in vec)

@pytest.mark.asyncio
@pytest.mark.integration
async def test_real_embed_empty_texts(real_client):
    if not await is_service_available():
        pytest.skip("Real service on localhost:8001 is not available.")
    result = await real_client.cmd("embed", params={"texts": []})
    vectors = extract_vectors(result)
    assert isinstance(vectors, list)
    assert len(vectors) == 0

@pytest.mark.asyncio
@pytest.mark.integration
async def test_real_cmd_invalid_command(real_client):
    if not await is_service_available():
        pytest.skip("Real service on localhost:8001 is not available.")
    with pytest.raises(EmbeddingServiceAPIError):
        await real_client.cmd("not_a_command")

@pytest.mark.asyncio
@pytest.mark.integration
async def test_real_invalid_endpoint():
    if not await is_service_available():
        pytest.skip("Real service on localhost:8001 is not available.")
    async with EmbeddingServiceAsyncClient(base_url=BASE_URL, port=PORT) as client:
        with pytest.raises(EmbeddingServiceHTTPError):
            # Пробуем обратиться к несуществующему endpoint
            url = f"{BASE_URL}:{PORT}/notfound"
            async with client._session.get(url) as resp:
                await client._raise_for_status(resp) 