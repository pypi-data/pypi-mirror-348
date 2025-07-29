"""
Tests for the Pipelines functionality in Zeebee AI SDK.
"""
import json
import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from zeebee_ai_client import ZeebeeClient
from zeebee_ai_client.exceptions import PipelineException

class TestPipelines:
    """Test suite for Pipelines functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.client = ZeebeeClient(api_key="test-api-key")
        self.pipeline_controller = self.client.pipelines
    
    @patch("requests.Session.post")
    def test_create_pipeline(self, mock_post):
        """Test create_pipeline method"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "pipeline_id": "test-pipeline-id",
            "name": "Test Pipeline",
            "stages": [
                {"agent_id": "agent-1", "name": "Stage 1"},
                {"agent_id": "agent-2", "name": "Stage 2"}
            ]
        }
        mock_post.return_value = mock_response
        
        # Test
        result = self.pipeline_controller.create_pipeline(
            name="Test Pipeline",
            stages=[
                {"agent_id": "agent-1", "name": "Stage 1"},
                {"agent_id": "agent-2", "name": "Stage 2"}
            ],
            description="A test pipeline"
        )
        
        # Assertions
        mock_post.assert_called_once()
        assert result["pipeline_id"] == "test-pipeline-id"
        assert result["name"] == "Test Pipeline"
        assert len(result["stages"]) == 2
    
    def test_create_pipeline_validation(self):
        """Test create_pipeline validation"""
        # Test empty name
        with pytest.raises(PipelineException) as excinfo:
            self.pipeline_controller.create_pipeline(
                name="",
                stages=[{"agent_id": "agent-1"}]
            )
        assert "Pipeline name cannot be empty" in str(excinfo.value)
        
        # Test invalid stages type
        with pytest.raises(PipelineException) as excinfo:
            self.pipeline_controller.create_pipeline(
                name="Test Pipeline",
                stages="not a list"  # Not a list
            )
        assert "Stages must be a list" in str(excinfo.value)
        
        # Test missing agent_id in stage
        with pytest.raises(PipelineException) as excinfo:
            self.pipeline_controller.create_pipeline(
                name="Test Pipeline",
                stages=[{"name": "Stage without agent_id"}]  # Missing agent_id
            )
        assert "is missing required field: agent_id" in str(excinfo.value)
    
    @patch("requests.Session.get")
    def test_get_pipeline(self, mock_get):
        """Test get_pipeline method"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "pipeline": {
                "id": "test-pipeline-id",
                "name": "Test Pipeline",
                "configuration": {
                    "stages": [
                        {"agent_id": "agent-1", "name": "Stage 1"},
                        {"agent_id": "agent-2", "name": "Stage 2"}
                    ]
                }
            }
        }
        mock_get.return_value = mock_response
        
        # Test
        result = self.pipeline_controller.get_pipeline("test-pipeline-id")
        
        # Assertions
        mock_get.assert_called_once()
        assert result["pipeline"]["id"] == "test-pipeline-id"
        assert result["pipeline"]["name"] == "Test Pipeline"
        assert len(result["pipeline"]["configuration"]["stages"]) == 2
    
    @patch("requests.Session.get")
    def test_get_pipelines(self, mock_get):
        """Test get_pipelines method"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "pipelines": [
                {"id": "pipeline-1", "name": "Pipeline 1"},
                {"id": "pipeline-2", "name": "Pipeline 2"}
            ],
            "total": 2
        }
        mock_get.return_value = mock_response
        
        # Test
        result = self.pipeline_controller.get_pipelines()
        
        # Assertions
        mock_get.assert_called_once()
        assert len(result["pipelines"]) == 2
        assert result["pipelines"][0]["name"] == "Pipeline 1"
        assert result["pipelines"][1]["name"] == "Pipeline 2"
    
    @patch("requests.Session.put")
    def test_update_pipeline(self, mock_put):
        """Test update_pipeline method"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "pipeline_id": "test-pipeline-id",
            "name": "Updated Pipeline",
            "stages": [
                {"agent_id": "agent-1", "name": "Stage 1"},
                {"agent_id": "agent-3", "name": "New Stage"}
            ]
        }
        mock_put.return_value = mock_response
        
        # Test
        result = self.pipeline_controller.update_pipeline(
            pipeline_id="test-pipeline-id",
            update_data={
                "name": "Updated Pipeline",
                "stages": [
                    {"agent_id": "agent-1", "name": "Stage 1"},
                    {"agent_id": "agent-3", "name": "New Stage"}
                ]
            }
        )
        
        # Assertions
        mock_put.assert_called_once()
        assert result["name"] == "Updated Pipeline"
        assert result["stages"][1]["name"] == "New Stage"
    
    @patch("requests.Session.delete")
    def test_delete_pipeline(self, mock_delete):
        """Test delete_pipeline method"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True}
        mock_delete.return_value = mock_response
        
        # Test
        result = self.pipeline_controller.delete_pipeline("test-pipeline-id")
        
        # Assertions
        mock_delete.assert_called_once()
        assert result["success"] is True
    
    @patch("requests.Session.post")
    def test_execute_pipeline(self, mock_post):
        """Test execute_pipeline method"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "execution_id": "test-execution-id",
            "status": "completed",
            "result": {"key": "Pipeline result"}
        }
        mock_post.return_value = mock_response
        
        # Test
        result = self.pipeline_controller.execute_pipeline(
            pipeline_id="test-pipeline-id",
            input_data={"query": "What is the weather?"},
            conversation_id="test-convo-id"
        )
        
        # Assertions
        mock_post.assert_called_once()
        assert result["execution_id"] == "test-execution-id"
        assert result["status"] == "completed"
        assert result["result"]["key"] == "Pipeline result"
    
    @patch("requests.Session.get")
    def test_get_pipeline_executions(self, mock_get):
        """Test get_pipeline_executions method"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "executions": [
                {"id": "exec-1", "status": "completed"},
                {"id": "exec-2", "status": "running"}
            ],
            "total": 2
        }
        mock_get.return_value = mock_response
        
        # Test
        result = self.pipeline_controller.get_pipeline_executions("test-pipeline-id")
        
        # Assertions
        mock_get.assert_called_once()
        assert len(result["executions"]) == 2
        assert result["executions"][0]["id"] == "exec-1"
        assert result["executions"][1]["status"] == "running"
    
    @patch("requests.Session.get")
    def test_get_execution(self, mock_get):
        """Test get_execution method"""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "execution": {
                "id": "test-execution-id",
                "status": "completed",
                "pipeline_id": "test-pipeline-id",
                "execution_time_ms": 1500,
                "stages": [
                    {"stage_name": "Stage 1", "status": "completed"},
                    {"stage_name": "Stage 2", "status": "completed"}
                ]
            }
        }
        mock_get.return_value = mock_response
        
        # Test
        result = self.pipeline_controller.get_execution("test-execution-id")
        
        # Assertions
        mock_get.assert_called_once()
        assert result["execution"]["id"] == "test-execution-id"
        assert result["execution"]["status"] == "completed"
        assert len(result["execution"]["stages"]) == 2
 