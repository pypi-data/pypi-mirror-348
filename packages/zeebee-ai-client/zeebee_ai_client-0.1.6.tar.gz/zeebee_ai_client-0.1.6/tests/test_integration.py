"""
Integration tests for the Zeebee AI SDK.

These tests demonstrate how the different components of the SDK work together.
They are designed to be run against mock responses.
"""
import pytest
from unittest.mock import patch, MagicMock

from zeebee_ai_client import ZeebeeClient, AgentTypes

class TestIntegration:
    """Integration test suite for the Zeebee AI SDK"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.client = ZeebeeClient(api_key="test-api-key")
    
    @patch("requests.Session.post")
    @patch("requests.Session.get")
    def test_create_and_execute_agent(self, mock_get, mock_post):
        """Test creating and executing an agent"""
        # Mock responses for agent creation
        create_response = MagicMock()
        create_response.json.return_value = {
            "agent_id": "test-agent-id",
            "name": "Web Search Agent",
            "agent_type": AgentTypes.WEB
        }
        
        # Mock response for agent execution
        execute_response = MagicMock()
        execute_response.json.return_value = {
            "result": "Paris is the capital of France",
            "execution_id": "test-execution-id"
        }
        
        # Configure mocks to return different responses based on the endpoint
        def post_side_effect(*args, **kwargs):
            if "/api/agent/agents" in args[0] and "execute" not in args[0]:
                return create_response
            elif "/execute" in args[0]:
                return execute_response
            return MagicMock()
            
        mock_post.side_effect = post_side_effect
        
        # Create the agent
        agent = self.client.agents.create_agent(
            name="Web Search Agent",
            agent_type=AgentTypes.WEB,
            configuration={"search_engine": "google", "num_results": 5}
        )
        
        # Execute the agent
        result = self.client.agents.execute_agent(
            agent_id=agent["agent_id"],
            input_data={"query": "What is the capital of France?"}
        )
        
        # Assertions
        assert agent["agent_id"] == "test-agent-id"
        assert agent["name"] == "Web Search Agent"
        assert result["result"] == "Paris is the capital of France"
    
    @patch("requests.Session.post")
    def test_create_and_execute_pipeline(self, mock_post):
        """Test creating and executing a pipeline"""
        # Mock responses for pipeline creation
        create_response = MagicMock()
        create_response.json.return_value = {
            "pipeline_id": "test-pipeline-id",
            "name": "Search and Summarize",
            "stages": [
                {"agent_id": "agent-1", "name": "Web Search"},
                {"agent_id": "agent-2", "name": "Summarize"}
            ]
        }
        
        # Mock response for pipeline execution
        execute_response = MagicMock()
        execute_response.json.return_value = {
            "execution_id": "test-execution-id",
            "status": "completed",
            "result": {
                "summary": "Paris is the capital of France. It is known for the Eiffel Tower."
            }
        }
        
        # Configure mocks to return different responses based on the endpoint
        def post_side_effect(*args, **kwargs):
            if "/api/agent/pipelines" in args[0] and "/execute" not in args[0]:
                return create_response
            elif "/execute" in args[0]:
                return execute_response
            return MagicMock()
            
        mock_post.side_effect = post_side_effect
        
        # Create the pipeline
        pipeline = self.client.pipelines.create_pipeline(
            name="Search and Summarize",
            stages=[
                {
                    "agent_id": "agent-1",
                    "name": "Web Search",
                    "input_mapping": {"query": "$.input.search_query"},
                    "output_mapping": {"search_results": "$.output.results"}
                },
                {
                    "agent_id": "agent-2",
                    "name": "Summarize",
                    "input_mapping": {"text": "$.stages.Web Search.search_results"},
                    "output_mapping": {"summary": "$.output.summary"}
                }
            ],
            description="Pipeline that searches the web and summarizes the results"
        )
        
        # Execute the pipeline
        result = self.client.pipelines.execute_pipeline(
            pipeline_id=pipeline["pipeline_id"],
            input_data={"search_query": "Tell me about Paris"}
        )
        
        # Assertions
        assert pipeline["pipeline_id"] == "test-pipeline-id"
        assert pipeline["name"] == "Search and Summarize"
        assert len(pipeline["stages"]) == 2
        assert result["status"] == "completed"
        assert "Paris is the capital of France" in result["result"]["summary"]
    
    @patch("requests.Session.post")
    def test_chat_with_layout(self, mock_post):
        """Test chat with dynamic layout generation"""
        # Mock responses for layout generation
        layout_response = MagicMock()
        layout_response.json.return_value = {
            "success": True,
            "layout": {
                "template": "dashboard",
                "type": "table-layout",
                "components": [
                    {"type": "table", "options": {"headers": ["City", "Population"]}}
                ]
            }
        }
        
        # Mock response for chat
        chat_response = MagicMock()
        chat_response.json.return_value = {
            "response": "Here's a table of city populations",
            "conversation_id": "test-convo-id",
            "layout_data": {
                "table": [
                    {"City": "Tokyo", "Population": "37.4 million"},
                    {"City": "Delhi", "Population": "29.4 million"},
                    {"City": "Shanghai", "Population": "26.3 million"}
                ]
            }
        }
        
        # Configure mocks to return different responses based on the endpoint
        def post_side_effect(*args, **kwargs):
            if "/api/routing/test/layout" in args[0]:
                return layout_response
            elif "/api/chat/completions" in args[0]:
                return chat_response
            return MagicMock()
            
        mock_post.side_effect = post_side_effect
        
        # First generate a layout based on the message
        layout = self.client.routing.generate_layout(
            message="Show me a table of the most populated cities in the world"
        )
        
        # Then use the generated layout in the chat
        response = self.client.chat(
            message="Show me a table of the most populated cities in the world",
            layout=layout["layout"]["template"]
        )
        
        # Assertions
        assert layout["layout"]["template"] == "dashboard"
        assert layout["layout"]["type"] == "table-layout"
        assert response["response"] == "Here's a table of city populations"
        assert response["layout_data"]["table"][0]["City"] == "Tokyo"
        assert len(response["layout_data"]["table"]) == 3
