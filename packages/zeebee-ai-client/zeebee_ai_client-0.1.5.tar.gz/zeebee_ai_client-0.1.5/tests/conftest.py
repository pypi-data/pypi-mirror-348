"""
Shared pytest fixtures for Zeebee AI SDK tests.
"""
import pytest
from unittest.mock import patch

@pytest.fixture
def mock_session():
    """Fixture to mock the requests Session"""
    with patch("requests.Session") as mock:
        yield mock

@pytest.fixture
def mock_env_api_key():
    """Fixture to mock the ZEEBEE_API_KEY environment variable"""
    with patch.dict("os.environ", {"ZEEBEE_API_KEY": "test-env-key"}):
        yield

@pytest.fixture
def sample_agent_config():
    """Sample agent configuration for testing"""
    return {
        "name": "Test Agent",
        "agent_type": "WebAgent",
        "configuration": {
            "search_engine": "google",
            "num_results": 5
        },
        "description": "A test agent for searching the web"
    }

@pytest.fixture
def sample_pipeline_config():
    """Sample pipeline configuration for testing"""
    return {
        "name": "Test Pipeline",
        "stages": [
            {
                "agent_id": "agent-1",
                "name": "Stage 1",
                "input_mapping": {"input1": "$.input.value1"},
                "output_mapping": {"output1": "$.output.result1"}
            },
            {
                "agent_id": "agent-2",
                "name": "Stage 2",
                "input_mapping": {"input2": "$.stages.Stage 1.output1"},
                "output_mapping": {"output2": "$.output.result2"}
            }
        ],
        "description": "A test pipeline with two stages"
    }
