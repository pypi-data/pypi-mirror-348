"""
Tests for the Routing functionality in Zeebee AI SDK.
"""
import pytest
from unittest.mock import patch, MagicMock

from zeebee_ai_client import ZeebeeClient, IntentCategory, LayoutType
from zeebee_ai_client.exceptions import RoutingException

class TestRouting:
    """Test suite for Routing functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.client = ZeebeeClient(api_key="test-api-key")
        self.routing_controller = self.client.routing
    
    def test_intent_category(self):
        """Test IntentCategory class"""
        # Verify intent categories are available
        assert IntentCategory.INFORMATION_RETRIEVAL == "INFORMATION_RETRIEVAL"
        assert IntentCategory.CONTENT_CREATION == "CONTENT_CREATION"
        assert IntentCategory.CODE_GENERATION == "CODE_GENERATION"
        assert IntentCategory.GENERAL_QUERY == "GENERAL_QUERY"
        
        # Test all() method
        all_intents = IntentCategory.all()
        assert len(all_intents) == 13
        assert IntentCategory.INFORMATION_RETRIEVAL in all_intents
        assert IntentCategory.CODE_GENERATION in all_intents
        assert IntentCategory.UNKNOWN in all_intents
    
    def test_layout_type(self):
        """Test LayoutType class"""
        # Verify layout types are available
        assert LayoutType.TEXT_HIGHLIGHT == "text-highlight"
        assert LayoutType.CODE_DISPLAY == "code"
        assert LayoutType.TABLE_LAYOUT == "dashboard"
        assert LayoutType.SIMPLE == "simple"
        
        # Test all() method
        all_layouts = LayoutType.all()
        assert len(all_layouts) == 11
        assert LayoutType.CODE_DISPLAY in all_layouts
        assert LayoutType.TABLE_LAYOUT in all_layouts
        assert LayoutType.SIMPLE in all_layouts
    
    @patch("requests.Session.post")
    def test_generate_layout(self, mock_post):
        """Test generate_layout method"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "layout": {
                "id": "layout-123",
                "template": "code",
                "type": "code-display",
                "theme": "dark",
                "responsive": True,
                "components": [
                    {"type": "header", "options": {"text": "Code Example"}},
                    {"type": "code", "options": {"language": "python"}}
                ],
                "content_analysis": {
                    "contentTypes": ["code", "explanation"],
                    "complexity": "medium"
                }
            },
            "scoring": {
                "level": "intermediate",
                "context": "programming",
                "inputType": "question",
                "scores": {
                    "CODE_GENERATION": 0.85,
                    "CODE_EXPLANATION": 0.75,
                    "GENERAL_QUERY": 0.2
                }
            }
        }
        mock_post.return_value = mock_response
        
        # Test with just a message
        result = self.routing_controller.generate_layout(
            message="Can you write a Python function to calculate Fibonacci numbers?"
        )
        
        # Assertions
        mock_post.assert_called_once()
        assert result["success"] is True
        assert result["layout"]["template"] == "code"
        assert result["layout"]["type"] == "code-display"
        assert len(result["layout"]["components"]) == 2
        assert result["scoring"]["scores"]["CODE_GENERATION"] == 0.85
        
        # Reset mock and test with routing result
        mock_post.reset_mock()
        mock_post.return_value = mock_response
        
        result = self.routing_controller.generate_layout(
            message="Can you write a Python function to calculate Fibonacci numbers?",
            routing_result={
                "suggested_template": "code",
                "content_analysis": {
                    "contentTypes": ["code", "explanation"],
                    "complexity": "medium"
                }
            }
        )
        
        # Assertions
        mock_post.assert_called_once()
        assert result["layout"]["template"] == "code"
    
    def test_generate_layout_validation(self):
        """Test generate_layout validation"""
        # Test empty message
        with pytest.raises(RoutingException) as excinfo:
            self.routing_controller.generate_layout(message="")
        assert "Message cannot be empty" in str(excinfo.value)
        
        # Test invalid message type
        with pytest.raises(RoutingException) as excinfo:
            self.routing_controller.generate_layout(message=123)  # Not a string
        assert "Message must be a string" in str(excinfo.value)
        
        # Test invalid routing_result type
        with pytest.raises(RoutingException) as excinfo:
            self.routing_controller.generate_layout(
                message="Hello",
                routing_result="not a dict"  # Not a dictionary
            )
        assert "Routing result must be a dictionary" in str(excinfo.value)
