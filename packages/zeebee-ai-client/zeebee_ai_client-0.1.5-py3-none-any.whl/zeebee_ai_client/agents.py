"""
Agent controller for the Zeebee AI Python SDK.
"""

from typing import Dict, List, Any, Optional
from .exceptions import AgentException

class AgentTypes:
    """
    Available agent types in the Zeebee AI platform.
    
    This class provides constants for all supported agent types to use when
    creating agents, making code more readable and less error-prone.
    """
    
    # Agent for retrieving information from knowledge bases
    RETRIEVAL = "RetrievalAgent"
    
    # Agent for summarizing long-form content
    SUMMARIZATION = "SummarizationAgent"
    
    # Agent for performing logical reasoning and analysis
    REASONING = "ReasoningAgent"
    
    # Agent for generating creative content
    GENERATION = "GenerationAgent"
    
    # Agent for interacting with web resources
    WEB = "WebAgent"
    
    # Agent for processing and transforming structured data
    STRUCTURE = "StructureAgent"
    
    @classmethod
    def all(cls) -> List[str]:
        """
        Returns a list of all available agent type names.
        
        Returns:
            List[str]: All available agent type names
        """
        return [
            cls.RETRIEVAL,
            cls.SUMMARIZATION, 
            cls.REASONING,
            cls.GENERATION,
            cls.WEB,
            cls.STRUCTURE
        ]

class AgentController:
    """Controller for agent operations."""
    
    def __init__(self, client):
        """
        Initialize the agent controller.
        
        Args:
            client: ZeebeeClient instance
        """
        self.client = client
        
        # Validate that client session exists
        if not hasattr(self.client, '_session'):
            raise AgentException("Client session not initialized. Make sure the ZeebeeClient is properly initialized.")
    
    def create_agent(
        self,
        name: str,
        agent_type: str,
        configuration: Dict[str, Any],
        description: Optional[str] = None,
        model_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a new agent.
        
        Args:
            name (str): Name of the agent to create (required)
                Example: "Web Search Agent"
                
            agent_type (str): Type of agent to create (required)
                Must be one of the available agent types
                Example: "WebAgent"
                
            configuration (Dict[str, Any]): Configuration for the agent (required)
                The structure depends on the agent type
                Example for WebAgent: {"search_engine": "google", "num_results": 5}
                
            description (Optional[str]): Optional description of the agent's purpose
                Example: "Agent that searches the web for information"
                
            model_id (Optional[str]): Optional model ID to use with this agent
                If not provided, agent will use the default model
                Example: "gpt-4o"
        
        Returns:
            Dict[str, Any]: Created agent details including its ID
            
        Raises:
            AgentException: If validation fails or server returns an error
            
        Example:
            ```python
            agent = agent_controller.create_agent(
                name="Web Search Agent",
                agent_type="WebAgent",
                configuration={"search_engine": "google", "num_results": 5},
                description="Agent that searches the web for information",
                model_id="gpt-4o"
            )
            print(f"Created agent with ID: {agent['agent_id']}")
            ```
        """
        # Validate input data
        self._validate_name(name)
        self._validate_optional_string(description, "Description", 1000)
        
        if not agent_type:
            raise AgentException("Agent type cannot be empty")
        
        if not isinstance(agent_type, str):
            raise AgentException("Agent type must be a string")
            
        if not isinstance(configuration, dict):
            raise AgentException("Configuration must be a dictionary")
            
        if model_id is not None and not isinstance(model_id, str):
            raise AgentException("Model ID must be a string")
            
        endpoint = f"{self.client.base_url}/api/agent/agents"
        
        payload = {
            "name": name,
            "agent_type": agent_type,
            "configuration": configuration
        }
        
        if description:
            payload["description"] = description
            
        if model_id:
            payload["model_id"] = model_id
            
        try:
            response = self.client._session.post(
                endpoint,
                headers=self.client._get_headers(),
                json=payload,
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise AgentException(f"Failed to create agent: {e}")
    
    def get_agent(self, agent_id: str) -> Dict[str, Any]:
        """
        Get agent details by ID.
        
        Args:
            agent_id (str): The unique identifier of the agent to retrieve (required)
                This is the ID returned when creating an agent
                Example: "550e8400-e29b-41d4-a716-446655440000"
            
        Returns:
            Dict[str, Any]: Agent details including configuration and metadata
            
        Raises:
            AgentException: If validation fails, agent doesn't exist, or server returns an error
            
        Example:
            ```python
            agent = agent_controller.get_agent("550e8400-e29b-41d4-a716-446655440000")
            print(f"Agent name: {agent['name']}")
            print(f"Agent type: {agent['agent_type']}")
            ```
        """
        # Validate input data
        if not agent_id:
            raise AgentException("Agent ID cannot be empty")
        
        if not isinstance(agent_id, str):
            raise AgentException("Agent ID must be a string")
        
        endpoint = f"{self.client.base_url}/api/agent/agents/{agent_id}"
        
        try:
            response = self.client._session.get(
                endpoint,
                headers=self.client._get_headers(),
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise AgentException(f"Failed to get agent: {e}")
    
    def update_agent(
        self,
        agent_id: str,
        update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing agent.
        
        Args:
            agent_id (str): The unique identifier of the agent to update (required)
                Example: "550e8400-e29b-41d4-a716-446655440000"
                
            update_data (Dict[str, Any]): Data to update on the agent (required)
                Only include fields you want to modify
                Supported fields:
                - name: New name for the agent
                - description: New description
                - configuration: Updated configuration dictionary
                - model_id: New model ID to use
                
                Example: {"name": "New Agent Name", "configuration": {"new_config": "value"}}
            
        Returns:
            Dict[str, Any]: Updated agent details
            
        Raises:
            AgentException: If validation fails, agent doesn't exist, you don't have 
                           permission to update it, or server returns an error
            
        Example:
            ```python
            updated_agent = agent_controller.update_agent(
                agent_id="550e8400-e29b-41d4-a716-446655440000",
                update_data={
                    "name": "Improved Web Agent",
                    "configuration": {"search_engine": "bing", "num_results": 10}
                }
            )
            print("Agent updated successfully")
            ```
        """
        # Validate input data
        if not agent_id:
            raise AgentException("Agent ID cannot be empty")
        
        if not isinstance(agent_id, str):
            raise AgentException("Agent ID must be a string")
        
        if not isinstance(update_data, dict):
            raise AgentException("Update data must be a dictionary")
        
        # Validate fields in update_data if they exist
        if 'name' in update_data:
            self._validate_name(update_data['name'])
            
        if 'description' in update_data:
            self._validate_optional_string(update_data['description'], "Description", 1000)
            
        if 'configuration' in update_data:
            self._validate_dict(update_data['configuration'], "Configuration")
            
        if 'model_id' in update_data and update_data['model_id'] is not None:
            self._validate_optional_string(update_data['model_id'], "Model ID", 100)
        
        endpoint = f"{self.client.base_url}/api/agent/agents/{agent_id}"
        
        try:
            response = self.client._session.put(
                endpoint,
                headers=self.client._get_headers(),
                json=update_data,
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise AgentException(f"Failed to update agent: {e}")
    
    def delete_agent(self, agent_id: str) -> Dict[str, Any]:
        """
        Delete an agent.
        
        Args:
            agent_id (str): The unique identifier of the agent to delete (required)
                Example: "550e8400-e29b-41d4-a716-446655440000"
            
        Returns:
            Dict[str, Any]: Deletion confirmation
            
        Raises:
            AgentException: If validation fails, agent doesn't exist, you don't have 
                           permission to delete it, or server returns an error
            
        Example:
            ```python
            result = agent_controller.delete_agent("550e8400-e29b-41d4-a716-446655440000")
            print("Agent deleted successfully")
            ```
        """
        # Validate input data
        if not agent_id:
            raise AgentException("Agent ID cannot be empty")
        
        if not isinstance(agent_id, str):
            raise AgentException("Agent ID must be a string")
        
        endpoint = f"{self.client.base_url}/api/agent/agents/{agent_id}"
        
        try:
            response = self.client._session.delete(
                endpoint,
                headers=self.client._get_headers(),
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise AgentException(f"Failed to delete agent: {e}")
            
    def execute_agent(
        self,
        agent_id: str,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute an agent with the provided input data.
        
        Args:
            agent_id (str): The unique identifier of the agent to execute (required)
                Example: "550e8400-e29b-41d4-a716-446655440000"
                
            input_data (Dict[str, Any]): Input data for the agent to process (required)
                The structure depends on the agent type
                Example for WebAgent: {"query": "What is the weather in New York?"}
                Example for StructureAgent: {"text": "Extract data from this text..."}
            
        Returns:
            Dict[str, Any]: Agent execution result
                The structure depends on the agent type
            
        Raises:
            AgentException: If validation fails, agent doesn't exist, you don't have 
                           permission to execute it, or server returns an error
            
        Example:
            ```python
            result = agent_controller.execute_agent(
                agent_id="550e8400-e29b-41d4-a716-446655440000",
                input_data={"query": "What is the weather in New York?"}
            )
            print(f"Agent response: {result['result']}")
            ```
        """
        # Validate input data
        if not agent_id:
            raise AgentException("Agent ID cannot be empty")
        
        if not isinstance(agent_id, str):
            raise AgentException("Agent ID must be a string")
        
        if not isinstance(input_data, dict):
            raise AgentException("Input data must be a dictionary")
        
        endpoint = f"{self.client.base_url}/api/agent/agents/{agent_id}/execute"
        
        try:
            response = self.client._session.post(
                endpoint,
                headers=self.client._get_headers(),
                json=input_data,
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise AgentException(f"Failed to execute agent: {e}")
            
    def get_agent_types(self) -> Dict[str, Any]:
        """
        Get all available agent types.
        
        Returns:
            Dict[str, Any]: List of available agent types with their descriptions
            
        Raises:
            AgentException: If server returns an error
            
        Example:
            ```python
            agent_types = agent_controller.get_agent_types()
            print("Available agent types:")
            for agent_type in agent_types["agent_types"]:
                print(f"- {agent_type}")
            ```
        """
        endpoint = f"{self.client.base_url}/api/agent/types"
        
        try:
            response = self.client._session.get(
                endpoint,
                headers=self.client._get_headers(),
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise AgentException(f"Failed to get agent types: {e}")
            
    def get_agents(self) -> Dict[str, Any]:
        """
        Get all agents available to the user.
        
        Returns:
            Dict[str, Any]: List of available agents with their metadata
                Includes both agents created by the user and public agents
            
        Raises:
            AgentException: If server returns an error
            
        Example:
            ```python
            agents = agent_controller.get_agents()
            print("My agents:")
            for agent in agents["agents"]:
                print(f"- {agent['name']} (ID: {agent['id']})")
            ```
        """
        endpoint = f"{self.client.base_url}/api/agent/agents"
        
        try:
            response = self.client._session.get(
                endpoint,
                headers=self.client._get_headers(),
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise AgentException(f"Failed to get agents: {e}")
            
    # Validation helper methods
    def _validate_name(self, name: str) -> None:
        """Validate a name field."""
        if not name:
            raise AgentException("Name cannot be empty")
        
        if not isinstance(name, str):
            raise AgentException("Name must be a string")
            
        if len(name) > 100:
            raise AgentException("Name cannot exceed 100 characters")
    
    def _validate_optional_string(self, value: Optional[str], field_name: str, max_length: int) -> None:
        """Validate an optional string field."""
        if value is not None:
            if not isinstance(value, str):
                raise AgentException(f"{field_name} must be a string")
                
            if len(value) > max_length:
                raise AgentException(f"{field_name} cannot exceed {max_length} characters")
    
    def _validate_stages(self, stages: List[Dict[str, Any]]) -> None:
        """Validate pipeline stages configuration."""
        if not isinstance(stages, list):
            raise AgentException("Stages must be a list")
            
        for i, stage in enumerate(stages):
            if not isinstance(stage, dict):
                raise AgentException(f"Stage {i+1} must be a dictionary")
                
            if 'agent_id' not in stage:
                raise AgentException(f"Stage {i+1} is missing required field: agent_id")
                
            if not isinstance(stage['agent_id'], str):
                raise AgentException(f"Stage {i+1} agent_id must be a string")
                
            # Validate optional fields if present
            if 'name' in stage and not isinstance(stage['name'], str):
                raise AgentException(f"Stage {i+1} name must be a string")
                
            if 'input_mapping' in stage and not isinstance(stage['input_mapping'], dict):
                raise AgentException(f"Stage {i+1} input_mapping must be a dictionary")
                
            if 'output_mapping' in stage and not isinstance(stage['output_mapping'], dict):
                raise AgentException(f"Stage {i+1} output_mapping must be a dictionary")
                
            if 'condition' in stage and not isinstance(stage['condition'], dict):
                raise AgentException(f"Stage {i+1} condition must be a dictionary")
    
    def _validate_dict(self, value: Any, field_name: str) -> None:
        """Validate a dictionary field."""
        if not isinstance(value, dict):
            raise AgentException(f"{field_name} must be a dictionary")
