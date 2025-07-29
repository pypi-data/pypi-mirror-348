"""
Pipeline controller for the Zeebee AI Python SDK.
"""

from typing import Dict, List, Any, Optional
import json
import asyncio
import websockets
from .exceptions import PipelineException

class PipelineController:
    """Controller for pipeline operations."""
    
    def __init__(self, client):
        """
        Initialize the pipeline controller.
        
        Args:
            client: ZeebeeClient instance
        """
        self.client = client
        
        # Validate that client session exists
        if not hasattr(self.client, '_session'):
            raise PipelineException("Client session not initialized. Make sure the ZeebeeClient is properly initialized.")
    
    def create_pipeline(
        self,
        name: str,
        stages: Optional[List[Dict[str, Any]]] = None,
        description: Optional[str] = None,
        visual_layout: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new pipeline of connected agents.
        
        Args:
            name (str): Name of the pipeline to create (required)
                Example: "Web Search and Summarize Pipeline"
                
            stages (Optional[List[Dict[str, Any]]]): List of pipeline stages
                Each stage is a dictionary with these fields:
                - agent_id: ID of the agent to use (required)
                - name: Name for this stage (optional)
                - input_mapping: How to map pipeline inputs to agent inputs (optional)
                - output_mapping: How to map agent outputs to pipeline outputs (optional)
                - condition: Conditions for when to run this stage (optional)
                
                Example: [
                    {
                        "agent_id": "550e8400-e29b-41d4-a716-446655440000",
                        "name": "Web Search",
                        "input_mapping": {"query": "$.input.search_query"},
                        "output_mapping": {"search_results": "$.output.results"}
                    },
                    {
                        "agent_id": "661f9511-f3ab-52e5-b827-557766551111",
                        "name": "Summarize",
                        "input_mapping": {"text": "$.stages.Web Search.search_results"},
                        "output_mapping": {"summary": "$.output.summary"}
                    }
                ]
                
            description (Optional[str]): Optional description of the pipeline's purpose
                Example: "Pipeline that searches the web and summarizes the results"
                
            visual_layout (Optional[Dict[str, Any]]): Optional visual layout information
                Used by the visual pipeline builder interface
                Example: {"nodes": [...], "edges": [...]}
            
        Returns:
            Dict[str, Any]: Created pipeline details including its ID
            
        Raises:
            PipelineException: If validation fails or server returns an error
            
        Example:
            ```python
            pipeline = pipeline_controller.create_pipeline(
                name="Search and Summarize",
                stages=[
                    {
                        "agent_id": "550e8400-e29b-41d4-a716-446655440000",
                        "name": "Web Search",
                        "input_mapping": {"query": "$.input.search_query"},
                        "output_mapping": {"search_results": "$.output.results"}
                    },
                    {
                        "agent_id": "661f9511-f3ab-52e5-b827-557766551111",
                        "name": "Summarize",
                        "input_mapping": {"text": "$.stages.Web Search.search_results"},
                        "output_mapping": {"summary": "$.output.summary"}
                    }
                ],
                description="Pipeline that searches the web and summarizes the results"
            )
            print(f"Created pipeline with ID: {pipeline['pipeline_id']}")
            ```
        """
        # Validate input parameters
        if not name:
            raise PipelineException("Pipeline name cannot be empty")
        
        if not isinstance(name, str):
            raise PipelineException("Name must be a string")
            
        if len(name) > 100:
            raise PipelineException("Name cannot exceed 100 characters")
            
        if description is not None and not isinstance(description, str):
            raise PipelineException("Description must be a string")
            
        if description is not None and len(description) > 1000:
            raise PipelineException("Description cannot exceed 1000 characters")
            
        if stages is not None:
            if not isinstance(stages, list):
                raise PipelineException("Stages must be a list")
                
            for i, stage in enumerate(stages):
                if not isinstance(stage, dict):
                    raise PipelineException(f"Stage {i+1} must be a dictionary")
                    
                if 'agent_id' not in stage:
                    raise PipelineException(f"Stage {i+1} is missing required field: agent_id")
                    
                if not isinstance(stage['agent_id'], str):
                    raise PipelineException(f"Stage {i+1} agent_id must be a string")
                    
                # Validate optional fields if present
                if 'name' in stage and not isinstance(stage['name'], str):
                    raise PipelineException(f"Stage {i+1} name must be a string")
                    
                if 'input_mapping' in stage and not isinstance(stage['input_mapping'], dict):
                    raise PipelineException(f"Stage {i+1} input_mapping must be a dictionary")
                    
                if 'output_mapping' in stage and not isinstance(stage['output_mapping'], dict):
                    raise PipelineException(f"Stage {i+1} output_mapping must be a dictionary")
                    
                if 'condition' in stage and not isinstance(stage['condition'], dict):
                    raise PipelineException(f"Stage {i+1} condition must be a dictionary")
        
        if visual_layout is not None and not isinstance(visual_layout, dict):
            raise PipelineException("Visual layout must be a dictionary")
        
        endpoint = f"{self.client.base_url}/api/agent/pipelines"
        
        payload = {
            "name": name
        }
        
        if description:
            payload["description"] = description
            
        if stages:
            payload["stages"] = stages
            
        if visual_layout:
            payload["visual_layout"] = visual_layout
            
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
            raise PipelineException(f"Failed to create pipeline: {e}")
    
    def get_pipeline(self, pipeline_id: str) -> Dict[str, Any]:
        """
        Get pipeline details by ID.
        
        Args:
            pipeline_id (str): The unique identifier of the pipeline to retrieve (required)
                Example: "770e8400-e29b-41d4-a716-446655440000"
            
        Returns:
            Dict[str, Any]: Pipeline details including stages, configuration and metadata
            
        Raises:
            PipelineException: If validation fails, pipeline doesn't exist, or server returns an error
            
        Example:
            ```python
            pipeline = pipeline_controller.get_pipeline("770e8400-e29b-41d4-a716-446655440000")
            print(f"Pipeline name: {pipeline['pipeline']['name']}")
            print(f"Number of stages: {len(pipeline['pipeline']['configuration']['stages'])}")
            ```
        """
        # Validate input data
        if not pipeline_id:
            raise PipelineException("Pipeline ID cannot be empty")
        
        if not isinstance(pipeline_id, str):
            raise PipelineException("Pipeline ID must be a string")
        
        endpoint = f"{self.client.base_url}/api/agent/pipelines/{pipeline_id}"
        
        try:
            response = self.client._session.get(
                endpoint,
                headers=self.client._get_headers(),
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise PipelineException(f"Failed to get pipeline: {e}")
    
    def get_pipelines(self) -> Dict[str, Any]:
        """
        Get all pipelines available to the current user.
        
        Returns:
            Dict[str, Any]: List of available pipelines with their metadata
            
        Raises:
            PipelineException: If server returns an error
            
        Example:
            ```python
            pipelines = pipeline_controller.get_pipelines()
            print("My pipelines:")
            for pipeline in pipelines["pipelines"]:
                print(f"- {pipeline['name']} (ID: {pipeline['id']})")
            ```
        """
        endpoint = f"{self.client.base_url}/api/agent/pipelines"
        
        try:
            response = self.client._session.get(
                endpoint,
                headers=self.client._get_headers(),
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise PipelineException(f"Failed to get pipelines: {e}")
    
    def update_pipeline(
        self,
        pipeline_id: str,
        update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing pipeline.
        
        Args:
            pipeline_id (str): The unique identifier of the pipeline to update (required)
                Example: "770e8400-e29b-41d4-a716-446655440000"
                
            update_data (Dict[str, Any]): Data to update on the pipeline (required)
                Only include fields you want to modify
                Supported fields:
                - name: New name for the pipeline
                - description: New description
                - stages: Updated list of pipeline stages
                - visual_layout: Updated visual layout information
                
                Example: {"name": "New Pipeline Name", "stages": [...]}
            
        Returns:
            Dict[str, Any]: Updated pipeline details
            
        Raises:
            PipelineException: If validation fails, pipeline doesn't exist, you don't have 
                           permission to update it, or server returns an error
            
        Example:
            ```python
            updated_pipeline = pipeline_controller.update_pipeline(
                pipeline_id="770e8400-e29b-41d4-a716-446655440000",
                update_data={
                    "name": "Improved Search and Summarize",
                    "stages": [
                        # Updated stages configuration...
                    ]
                }
            )
            print("Pipeline updated successfully")
            ```
        """
        # Validate input data
        if not pipeline_id:
            raise PipelineException("Pipeline ID cannot be empty")
        
        if not isinstance(pipeline_id, str):
            raise PipelineException("Pipeline ID must be a string")
        
        if not isinstance(update_data, dict):
            raise PipelineException("Update data must be a dictionary")
        
        # Validate fields in update_data if they exist
        if 'name' in update_data:
            if not update_data['name']:
                raise PipelineException("Pipeline name cannot be empty")
            if not isinstance(update_data['name'], str):
                raise PipelineException("Pipeline name must be a string")
            if len(update_data['name']) > 100:
                raise PipelineException("Pipeline name cannot exceed 100 characters")
            
        if 'description' in update_data and update_data['description'] is not None:
            if not isinstance(update_data['description'], str):
                raise PipelineException("Description must be a string")
            if len(update_data['description']) > 1000:
                raise PipelineException("Description cannot exceed 1000 characters")
            
        if 'stages' in update_data:
            if not isinstance(update_data['stages'], list):
                raise PipelineException("Stages must be a list")
                
            for i, stage in enumerate(update_data['stages']):
                if not isinstance(stage, dict):
                    raise PipelineException(f"Stage {i+1} must be a dictionary")
                    
                if 'agent_id' not in stage:
                    raise PipelineException(f"Stage {i+1} is missing required field: agent_id")
                    
                if not isinstance(stage['agent_id'], str):
                    raise PipelineException(f"Stage {i+1} agent_id must be a string")
                    
                # Validate optional fields if present
                if 'name' in stage and not isinstance(stage['name'], str):
                    raise PipelineException(f"Stage {i+1} name must be a string")
                    
                if 'input_mapping' in stage and not isinstance(stage['input_mapping'], dict):
                    raise PipelineException(f"Stage {i+1} input_mapping must be a dictionary")
                    
                if 'output_mapping' in stage and not isinstance(stage['output_mapping'], dict):
                    raise PipelineException(f"Stage {i+1} output_mapping must be a dictionary")
                    
                if 'condition' in stage and not isinstance(stage['condition'], dict):
                    raise PipelineException(f"Stage {i+1} condition must be a dictionary")
            
        if 'visual_layout' in update_data and not isinstance(update_data['visual_layout'], dict):
            raise PipelineException("Visual layout must be a dictionary")
        
        endpoint = f"{self.client.base_url}/api/agent/pipelines/{pipeline_id}"
        
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
            raise PipelineException(f"Failed to update pipeline: {e}")
    
    def delete_pipeline(self, pipeline_id: str) -> Dict[str, Any]:
        """
        Delete a pipeline.
        
        Args:
            pipeline_id (str): The unique identifier of the pipeline to delete (required)
                Example: "770e8400-e29b-41d4-a716-446655440000"
            
        Returns:
            Dict[str, Any]: Deletion confirmation
            
        Raises:
            PipelineException: If validation fails, pipeline doesn't exist, you don't have 
                           permission to delete it, or server returns an error
            
        Example:
            ```python
            result = pipeline_controller.delete_pipeline("770e8400-e29b-41d4-a716-446655440000")
            print("Pipeline deleted successfully")
            ```
        """
        # Validate input data
        if not pipeline_id:
            raise PipelineException("Pipeline ID cannot be empty")
        
        if not isinstance(pipeline_id, str):
            raise PipelineException("Pipeline ID must be a string")
        
        endpoint = f"{self.client.base_url}/api/agent/pipelines/{pipeline_id}"
        
        try:
            response = self.client._session.delete(
                endpoint,
                headers=self.client._get_headers(),
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise PipelineException(f"Failed to delete pipeline: {e}")
            
    def execute_pipeline(
        self,
        pipeline_id: str,
        input_data: Dict[str, Any],
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Execute a pipeline with the provided input data.
        
        Args:
            pipeline_id (str): The unique identifier of the pipeline to execute (required)
                Example: "770e8400-e29b-41d4-a716-446655440000"
                
            input_data (Dict[str, Any]): Input data for the pipeline to process (required)
                The structure depends on the pipeline's input_mapping configuration
                Example: {"search_query": "What is the capital of France?"}
                
            conversation_id (Optional[str]): Optional conversation ID to link this execution to
                If provided, the execution will be associated with the conversation
                Example: "990e8400-e29b-41d4-a716-446655440000"
            
        Returns:
            Dict[str, Any]: Pipeline execution result
                Contains the final output of the pipeline and execution metadata
            
        Raises:
            PipelineException: If validation fails, pipeline doesn't exist, you don't have 
                           permission to execute it, or server returns an error
            
        Example:
            ```python
            result = pipeline_controller.execute_pipeline(
                pipeline_id="770e8400-e29b-41d4-a716-446655440000",
                input_data={"search_query": "What is the capital of France?"}
            )
            print(f"Pipeline result: {result['result']}")
            ```
        """
        # Validate input data
        if not pipeline_id:
            raise PipelineException("Pipeline ID cannot be empty")
        
        if not isinstance(pipeline_id, str):
            raise PipelineException("Pipeline ID must be a string")
        
        if not isinstance(input_data, dict):
            raise PipelineException("Input data must be a dictionary")
        
        if conversation_id is not None and not isinstance(conversation_id, str):
            raise PipelineException("Conversation ID must be a string")
        
        endpoint = f"{self.client.base_url}/api/agent/pipelines/{pipeline_id}/execute"
        
        payload = input_data.copy()
        if conversation_id:
            payload["conversation_id"] = conversation_id
            
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
            raise PipelineException(f"Failed to execute pipeline: {e}")
    
    def get_pipeline_executions(self, pipeline_id: str) -> Dict[str, Any]:
        """
        Get all executions of a pipeline.
        
        Args:
            pipeline_id (str): The unique identifier of the pipeline (required)
                Example: "770e8400-e29b-41d4-a716-446655440000"
            
        Returns:
            Dict[str, Any]: List of pipeline executions with their status and metadata
            
        Raises:
            PipelineException: If validation fails, pipeline doesn't exist, you don't have 
                           permission to access it, or server returns an error
            
        Example:
            ```python
            executions = pipeline_controller.get_pipeline_executions("770e8400-e29b-41d4-a716-446655440000")
            print(f"Found {len(executions['executions'])} execution(s):")
            for execution in executions['executions']:
                print(f"- ID: {execution['id']}, Status: {execution['status']}")
            ```
        """
        # Validate input data
        if not pipeline_id:
            raise PipelineException("Pipeline ID cannot be empty")
        
        if not isinstance(pipeline_id, str):
            raise PipelineException("Pipeline ID must be a string")
        
        endpoint = f"{self.client.base_url}/api/agent/pipelines/{pipeline_id}/executions"
        
        try:
            response = self.client._session.get(
                endpoint,
                headers=self.client._get_headers(),
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise PipelineException(f"Failed to get pipeline executions: {e}")
            
    def get_execution(self, execution_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific pipeline execution.
        
        Args:
            execution_id (str): The unique identifier of the execution to retrieve (required)
                Example: "880e8400-e29b-41d4-a716-446655440000"
            
        Returns:
            Dict[str, Any]: Detailed execution information including:
                - Status
                - Input/output data
                - Execution time
                - Stage-by-stage execution details
                - Error messages (if any)
            
        Raises:
            PipelineException: If validation fails, execution doesn't exist, you don't have 
                           permission to access it, or server returns an error
            
        Example:
            ```python
            execution = pipeline_controller.get_execution("880e8400-e29b-41d4-a716-446655440000")
            print(f"Execution status: {execution['execution']['status']}")
            print(f"Total execution time: {execution['execution']['execution_time_ms']}ms")
            print("Stage results:")
            for stage in execution['execution']['stages']:
                print(f"- {stage['stage_name']}: {stage['status']}")
            ```
        """
        # Validate input data
        if not execution_id:
            raise PipelineException("Execution ID cannot be empty")
        
        if not isinstance(execution_id, str):
            raise PipelineException("Execution ID must be a string")
        
        endpoint = f"{self.client.base_url}/api/agent/executions/{execution_id}"
        
        try:
            response = self.client._session.get(
                endpoint,
                headers=self.client._get_headers(),
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            return response.json()
            
        except Exception as e:
            raise PipelineException(f"Failed to get execution: {e}")
    
    async def execute_pipeline_streaming(
        self,
        pipeline_id: str,
        input_data: Dict[str, Any],
        conversation_id: Optional[str] = None
    ):
        """
        Execute a pipeline and stream the results in real-time.
        
        Args:
            pipeline_id (str): The unique identifier of the pipeline to execute
                Example: "770e8400-e29b-41d4-a716-446655440000"
                
            input_data (Dict[str, Any]): Input data for the pipeline to process
                Example: {"search_query": "What is the capital of France?"}
                
            conversation_id (Optional[str]): Optional conversation ID to link this execution to
                Example: "990e8400-e29b-41d4-a716-446655440000"
            
        Yields:
            Dict[str, Any]: Pipeline execution results in real-time
            
        Raises:
            PipelineException: If there's an error executing the pipeline or streaming results
            
        Example:
            ```python
            async for result in pipeline_controller.execute_pipeline_streaming(
                pipeline_id="770e8400-e29b-41d4-a716-446655440000",
                input_data={"search_query": "What is the capital of France?"}
            ):
                print(f"Stage: {result.get('stage_name')}, Status: {result.get('status')}")
            ```
        """
        # Validate input data
        if not pipeline_id:
            raise PipelineException("Pipeline ID cannot be empty")
        
        if not isinstance(pipeline_id, str):
            raise PipelineException("Pipeline ID must be a string")
        
        if not isinstance(input_data, dict):
            raise PipelineException("Input data must be a dictionary")
        
        if conversation_id is not None and not isinstance(conversation_id, str):
            raise PipelineException("Conversation ID must be a string")
        
        payload = input_data.copy()
        if conversation_id:
            payload["conversation_id"] = conversation_id
        
        # Send execute request to get execution ID
        endpoint = f"{self.client.base_url}/api/agent/pipelines/{pipeline_id}/execute/stream"
        
        try:
            response = self.client._session.post(
                endpoint,
                headers=self.client._get_headers(),
                json=payload,
                timeout=self.client.timeout
            )
            
            self.client._handle_error_response(response)
            result = response.json()
            
            execution_id = result.get("execution_id")
            if not execution_id:
                raise PipelineException("No execution ID returned from execute request")
            
            # Stream results from the execution
            async for update in self.listen_to_execution(execution_id):
                yield update
                
        except Exception as e:
            raise PipelineException(f"Failed to execute pipeline with streaming: {e}")
