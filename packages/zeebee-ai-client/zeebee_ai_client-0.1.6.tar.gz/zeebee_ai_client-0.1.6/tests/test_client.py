"""
Tests for the ZeebeeClient class.
"""
import os
import pytest
import json
from unittest.mock import patch, MagicMock

from zeebee_ai_client import ZeebeeClient
from zeebee_ai_client.exceptions import AuthenticationError, RateLimitError

class TestZeebeeClient:
    """Test suite for ZeebeeClient"""
    
    def test_init_with_api_key(self):
        """Test client initialization with API key"""
        client = ZeebeeClient(api_key="test-api-key")
        assert client.api_key == "test-api-key"
        
    def test_init_with_env_var(self):
        """Test client initialization with environment variable"""
        with patch.dict(os.environ, {"ZEEBEE_API_KEY": "env-api-key"}):
            client = ZeebeeClient()
            assert client.api_key == "env-api-key"
            
    @patch("requests.post")
    def test_chat(self, mock_post):
        """Test chat method"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "response": "Hello!",
            "conversation_id": "test-convo-id"
        }
        mock_post.return_value = mock_response
        
        # Test
        client = ZeebeeClient(api_key="test-api-key")
        result = client.chat(message="Hi", model="gpt-4o")
        
        # Assertions
        mock_post.assert_called_once()
        assert result["response"] == "Hello!"
        assert result["conversation_id"] == "test-convo-id"
        
    @patch("requests.post")
    def test_chat_with_system_prompt(self, mock_post):
        """Test chat with system prompt"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "response": "System prompted response",
            "conversation_id": "test-convo-id"
        }
        mock_post.return_value = mock_response
        
        # Test
        client = ZeebeeClient(api_key="test-api-key")
        result = client.chat(
            message="Hi", 
            model="gpt-4o", 
            system_prompt="You are a helpful assistant"
        )
        
        # Assertions
        mock_post.assert_called_once()
        assert result["response"] == "System prompted response"
        
        # Check that the system prompt was included in the request
        call_args = mock_post.call_args[1]
        request_data = call_args["json"]
        assert any(msg["role"] == "system" for msg in request_data["messages"])
        
    @patch("requests.post")
    def test_chat_with_stream(self, mock_post):
        """Test streaming chat"""
        # Setup mock for streamed response
        mock_response = MagicMock()
        mock_response.iter_lines.return_value = [
            b'data: {"chunk": "Hello", "conversation_id": "test-convo-id"}',
            b'data: {"chunk": " world", "conversation_id": "test-convo-id"}',
            b'data: [DONE]'
        ]
        mock_post.return_value = mock_response
        
        # Test
        client = ZeebeeClient(api_key="test-api-key")
        chunks = list(client.chat(message="Hi", model="gpt-4o", stream=True))
        
        # Assertions
        assert len(chunks) == 2
        assert chunks[0]["chunk"] == "Hello"
        assert chunks[1]["chunk"] == " world"
        
    @patch("requests.post")
    def test_authentication_error(self, mock_post):
        """Test authentication error handling"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": "Invalid API key"}
        mock_post.return_value = mock_response
        
        # Test
        client = ZeebeeClient(api_key="invalid-key")
        
        # Expect an authentication error
        with pytest.raises(AuthenticationError):
            client.chat(message="Hi")
            
    @patch("requests.post")
    def test_rate_limit_error(self, mock_post):
        """Test rate limit error handling"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.json.return_value = {"error": "Too many requests"}
        mock_post.return_value = mock_response
        
        # Test
        client = ZeebeeClient(api_key="test-api-key")
        
        # Expect a rate limit error
        with pytest.raises(RateLimitError):
            client.chat(message="Hi")
            
    @patch("requests.get")
    def test_get_conversation(self, mock_get):
        """Test get_conversation method"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "conversation": {
                "id": "test-convo-id",
                "title": "Test Conversation",
                "messages": [
                    {"role": "user", "content": "Hello"},
                    {"role": "assistant", "content": "Hi there!"}
                ]
            }
        }
        mock_get.return_value = mock_response
        
        # Test
        client = ZeebeeClient(api_key="test-api-key")
        result = client.get_conversation("test-convo-id")
        
        # Assertions
        mock_get.assert_called_once()
        assert result["conversation"]["id"] == "test-convo-id"
        assert len(result["conversation"]["messages"]) == 2
        
    @patch("requests.get")
    def test_list_conversations(self, mock_get):
        """Test list_conversations method"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "conversations": [
                {"id": "convo-1", "title": "Conversation 1"},
                {"id": "convo-2", "title": "Conversation 2"}
            ],
            "total": 2
        }
        mock_get.return_value = mock_response
        
        # Test
        client = ZeebeeClient(api_key="test-api-key")
        result = client.list_conversations(limit=10)
        
        # Assertions
        mock_get.assert_called_once()
        assert len(result["conversations"]) == 2
        assert result["total"] == 2
