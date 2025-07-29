"""
Autonomous Routing Controller for the Zeebee AI Python SDK.

This module provides client-side access to the Autonomous Routing system,
allowing applications to intelligently route user messages to appropriate
agents, pipelines, or models based on detected intents and context.
"""

from typing import Dict, Any
from .exceptions import RoutingException

class RoutingController:
    """Controller for autonomous routing operations."""
    
    def __init__(self, client):
        """
        Initialize the routing controller.
        
        Args:
            client: ZeebeeClient instance
        """
        self.client = client
        
        # Validate that client session exists
        if not hasattr(self.client, '_session'):
            raise RoutingException("Client session not initialized. Make sure the ZeebeeClient is properly initialized.")
    
    def route_message(
        self, 
        message: str
    ) -> Dict[str, Any]:
        """
        Route a user message to the appropriate agent, pipeline, or model.
        
        Args:
            message (str): The user message to route (required)
                
        Returns:
            Dict[str, Any]: Routing result with fields:
                - success: Whether the request was successful
                - route_to: Target destination (agent, pipeline, or model name)
                - route_type: Type of destination ("agent", "pipeline", or "model")
                - confidence: Confidence score (0-1)
                - intent: Intent information
                - reasoning: Reasons behind the routing decision
                - alternative_routes: Alternative routing options
                - diagnostic_info: Additional diagnostics
                
        Raises:
            RoutingException: If validation fails or server returns an error
            
        Example:
            ```python
            result = routing_controller.route_message(
                message="Write a function to sort a list in Python"
            )
            print(f"Routing to: {result['route_to']} ({result['route_type']})")
            print(f"Confidence: {result['confidence']}")
            ```
        """
        # Validate input data
        if not message:
            raise RoutingException("Message cannot be empty")
        
        if not isinstance(message, str):
            raise RoutingException("Message must be a string")
        
        # Prepare request payload
        payload = {
            "message": message
        }
        
        # Send request to route endpoint
        endpoint = f"{self.client.base_url}/api/routing/route"
        
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
            raise RoutingException(f"Failed to route message: {e}")
