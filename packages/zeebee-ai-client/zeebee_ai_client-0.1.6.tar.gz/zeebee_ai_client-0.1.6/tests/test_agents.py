"""
Tests for the Agents functionality in Zeebee AI SDK.
"""
import pytest
from unittest.mock import patch, MagicMock

from zeebee_ai_client import ZeebeeClient, AgentTypes
from zeebee_ai_client.exceptions import AgentException

class TestAgents:
    """Test suite for Agents functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.client = ZeebeeClient(api_key="test-api-key")
        self.agent_controller = self.client.agents
    
    def test_agent_types(self):
        """Test AgentTypes class"""
        # Verify all agent types are available
        assert AgentTypes.RETRIEVAL == "RetrievalAgent"
        assert AgentTypes.SUMMARIZATION == "SummarizationAgent"
        assert AgentTypes.REASONING == "ReasoningAgent"
        assert AgentTypes.GENERATION == "GenerationAgent"
        assert AgentTypes.WEB == "WebAgent"
        assert AgentTypes.STRUCTURE == "StructureAgent"
        
        # Test all() method
        all_types = AgentTypes.all()
        assert len(all_types) == 6
        assert AgentTypes.RETRIEVAL in all_types
        assert AgentTypes.WEB in all_types
    
    @patch("requests.Session.post")
    def test_create_agent(self, mock_post):
        """Test create_agent method"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "agent_id": "test-agent-id",
            "name": "Test Agent",
            "agent_type": AgentTypes.WEB,
            "configuration": {"search_engine": "google"}
        }
        mock_post.return_value = mock_response
        
        # Test
        result = self.agent_controller.create_agent(
            name="Test Agent",
            agent_type=AgentTypes.WEB,
            configuration={"search_engine": "google"},
            description="A test agent",
            model_id="gpt-4o"
        )
        
        # Assertions
        mock_post.assert_called_once()
        assert result["agent_id"] == "test-agent-id"
        assert result["name"] == "Test Agent"
        assert result["agent_type"] == AgentTypes.WEB
    
    def test_create_agent_validation(self):
        """Test create_agent validation"""
        # Test empty name
        with pytest.raises(AgentException) as excinfo:
            self.agent_controller.create_agent(
                name="",
                agent_type=AgentTypes.WEB,
                configuration={"search_engine": "google"}
            )
        assert "Name cannot be empty" in str(excinfo.value)
        
        # Test invalid agent_type type
        with pytest.raises(AgentException) as excinfo:
            self.agent_controller.create_agent(
                name="Test Agent",
                agent_type=123,  # Not a string
                configuration={"search_engine": "google"}
            )
        assert "Agent type must be a string" in str(excinfo.value)
        
        # Test invalid configuration type
        with pytest.raises(AgentException) as excinfo:
            self.agent_controller.create_agent(
                name="Test Agent",
                agent_type=AgentTypes.WEB,
                configuration="not a dict"  # Not a dictionary
            )
        assert "Configuration must be a dictionary" in str(excinfo.value)
    
    @patch("requests.Session.get")
    def test_get_agent(self, mock_get):
        """Test get_agent method"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "agent_id": "test-agent-id",
            "name": "Test Agent",
            "agent_type": AgentTypes.WEB,
            "configuration": {"search_engine": "google"}
        }
        mock_get.return_value = mock_response
        
        # Test
        result = self.agent_controller.get_agent("test-agent-id")
        
        # Assertions
        mock_get.assert_called_once()
        assert result["agent_id"] == "test-agent-id"
        assert result["name"] == "Test Agent"
    
    @patch("requests.Session.put")
    def test_update_agent(self, mock_put):
        """Test update_agent method"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "agent_id": "test-agent-id",
            "name": "Updated Agent",
            "agent_type": AgentTypes.WEB,
            "configuration": {"search_engine": "bing"}
        }
        mock_put.return_value = mock_response
        
        # Test
        result = self.agent_controller.update_agent(
            agent_id="test-agent-id",
            update_data={
                "name": "Updated Agent",
                "configuration": {"search_engine": "bing"}
            }
        )
        
        # Assertions
        mock_put.assert_called_once()
        assert result["name"] == "Updated Agent"
        assert result["configuration"]["search_engine"] == "bing"
    
    @patch("requests.Session.delete")
    def test_delete_agent(self, mock_delete):
        """Test delete_agent method"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True}
        mock_delete.return_value = mock_response
        
        # Test
        result = self.agent_controller.delete_agent("test-agent-id")
        
        # Assertions
        mock_delete.assert_called_once()
        assert result["success"] is True
    
    @patch("requests.Session.post")
    def test_execute_agent(self, mock_post):
        """Test execute_agent method"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "result": "Agent execution result",
            "execution_id": "test-execution-id"
        }
        mock_post.return_value = mock_response
        
        # Test
        result = self.agent_controller.execute_agent(
            agent_id="test-agent-id",
            input_data={"query": "What is the weather?"}
        )
        
        # Assertions
        mock_post.assert_called_once()
        assert result["result"] == "Agent execution result"
        assert result["execution_id"] == "test-execution-id"
    
    @patch("requests.Session.get")
    def test_get_agent_types(self, mock_get):
        """Test get_agent_types method"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "agent_types": [
                {"id": "RetrievalAgent", "name": "Retrieval Agent"},
                {"id": "WebAgent", "name": "Web Agent"}
            ]
        }
        mock_get.return_value = mock_response
        
        # Test
        result = self.agent_controller.get_agent_types()
        
        # Assertions
        mock_get.assert_called_once()
        assert len(result["agent_types"]) == 2
        assert result["agent_types"][0]["id"] == "RetrievalAgent"
        assert result["agent_types"][1]["id"] == "WebAgent"
