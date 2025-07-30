import sys
import types
import pytest
import asyncio
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_example_async_usage(monkeypatch):
    # Подменяем sys.argv для передачи base_url и порта
    monkeypatch.setattr(sys, 'argv', ['example_async_usage.py', '--base-url', 'http://test', '--port', '8001'])
    # Мокаем EmbeddingServiceAsyncClient и его методы
    with patch('embed_client.example_async_usage.EmbeddingServiceAsyncClient.__aenter__', new=AsyncMock(return_value=AsyncMock())), \
         patch('embed_client.example_async_usage.EmbeddingServiceAsyncClient.health', new=AsyncMock(return_value={"status": "ok"})):
        # Импортируем как модуль, чтобы выполнить main()
        import importlib
        import embed_client.example_async_usage as example
        importlib.reload(example)
        await example.main()

@pytest.mark.asyncio
async def test_example_async_usage_no_base_url(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['example_async_usage.py'])
    with patch('builtins.print') as mock_print, patch('sys.exit') as mock_exit:
        import importlib
        import embed_client.example_async_usage as example
        importlib.reload(example)
        await example.main()
        mock_print.assert_called()
        mock_exit.assert_called() 