"""
Dynamic Layout Engine for the Zeebee AI Python SDK.

This module provides client-side access to the Dynamic Layout system,
allowing applications to intelligently generate appropriate layouts for content
based on message complexity, detected intents and context.
"""

from typing import Dict, List, Any, Optional, Union
from .exceptions import RoutingException

class IntentCategory:
    """
    Available intent categories in the Zeebee AI routing system.
    
    This class provides constants for all supported intent categories,
    making code more readable and less error-prone when working with
    the routing system.
    """
    
    # Information seeking intents
    INFORMATION_RETRIEVAL = "INFORMATION_RETRIEVAL"
    
    # Content generation intents
    CONTENT_CREATION = "CONTENT_CREATION"
    CONTENT_SUMMARIZATION = "CONTENT_SUMMARIZATION"
    
    # Code-related intents
    CODE_GENERATION = "CODE_GENERATION"
    CODE_EXPLANATION = "CODE_EXPLANATION"
    
    # Analysis intents
    DATA_ANALYSIS = "DATA_ANALYSIS"
    SENTIMENT_ANALYSIS = "SENTIMENT_ANALYSIS"
    
    # Specialized intents
    TRANSLATION = "TRANSLATION"
    PERSONAL_ASSISTANCE = "PERSONAL_ASSISTANCE"
    CUSTOMER_SUPPORT = "CUSTOMER_SUPPORT"
    
    # System intents
    SYSTEM_INSTRUCTION = "SYSTEM_INSTRUCTION"
    
    # Fallback intent
    GENERAL_QUERY = "GENERAL_QUERY"
    
    # Unknown intent
    UNKNOWN = "UNKNOWN"
    
    @classmethod
    def all(cls) -> List[str]:
        """
        Returns a list of all available intent category values.
        
        Returns:
            List[str]: All available intent category values
        """
        return [
            cls.INFORMATION_RETRIEVAL,
            cls.CONTENT_CREATION,
            cls.CONTENT_SUMMARIZATION,
            cls.CODE_GENERATION,
            cls.CODE_EXPLANATION,
            cls.DATA_ANALYSIS,
            cls.SENTIMENT_ANALYSIS,
            cls.TRANSLATION,
            cls.PERSONAL_ASSISTANCE,
            cls.CUSTOMER_SUPPORT,
            cls.SYSTEM_INSTRUCTION,
            cls.GENERAL_QUERY,
            cls.UNKNOWN
        ]


class LayoutType:
    """
    Available layout types for the dynamic layout engine.
    
    This class provides constants for all supported layout types to use when
    requesting or specifying layout preferences.
    """
    
    # Simple text layout
    TEXT_HIGHLIGHT = "text-highlight"
    
    # List layouts
    CARD_LIST = "card-list"
    STACKED_CARDS = "stacked-cards"
    
    # Comparison layout
    COMPARISON_VIEW = "split"
    
    # Code display layout
    CODE_DISPLAY = "code"
    
    # Data visualization layout
    DATA_VISUALIZATION = "chart"
    
    # Document and story layouts
    STORY_BLOCK = "document"
    
    # Tabular data layout
    TABLE_LAYOUT = "dashboard"
    
    # Media gallery layout
    CAROUSEL_GALLERY = "media"
    
    # Timeline layout
    HERO_ALERT = "timeline"
    
    # Simple layout (default)
    SIMPLE = "simple"
    
    @classmethod
    def all(cls) -> List[str]:
        """
        Returns a list of all available layout type values.
        
        Returns:
            List[str]: All available layout type values
        """
        return [
            cls.TEXT_HIGHLIGHT,
            cls.CARD_LIST,
            cls.STACKED_CARDS,
            cls.COMPARISON_VIEW,
            cls.CODE_DISPLAY,
            cls.DATA_VISUALIZATION,
            cls.STORY_BLOCK,
            cls.TABLE_LAYOUT,
            cls.CAROUSEL_GALLERY,
            cls.HERO_ALERT,
            cls.SIMPLE
        ]


class LayoutController:
    """Controller for dynamic layout generation operations."""
    
    def __init__(self, client):
        """
        Initialize the layout controller.
        
        Args:
            client: ZeebeeClient instance
        """
        self.client = client
        
        # Validate that client session exists
        if not hasattr(self.client, '_session'):
            raise RoutingException("Client session not initialized. Make sure the ZeebeeClient is properly initialized.")
    
    def generate_layout(
        self,
        message: str,
        routing_result: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a dynamic layout based on message complexity and routing.
        
        Args:
            message (str): The user message to analyze (required)
                Example: "Can you create a table comparing different programming languages?"
                
            routing_result (Optional[Dict[str, Any]]): Optional routing result
                If provided, the layout will be customized based on the routing decision
                Example: {
                    "suggested_template": "dashboard", 
                    "content_analysis": {
                        "contentTypes": ["table", "comparison"],
                        "complexity": "medium",
                        "formality": "formal"
                    }
                }
            
        Returns:
            Dict[str, Any]: Layout configuration including:
                - success: Whether the request was successful
                - layout: Layout configuration containing:
                  - id: Unique layout identifier
                  - template: Template name (e.g., "simple", "code", "dashboard")
                  - type: Layout type (e.g., "text-highlight", "card-list")
                  - theme: Visual theme for the layout
                  - responsive: Whether the layout is responsive
                  - responsive_behavior: Breakpoint configurations
                  - components: List of UI components with options:
                    - type: Component type (e.g., "header", "text", "table")
                    - options: Component-specific options
                  - content_analysis: Content type and complexity analysis
                  - extracted_content: Content extracted from user message
                  - preview_settings: Settings for preview visualization
                  - version: Layout schema version
                - scoring: Message complexity analysis results including:
                  - level: Complexity level
                  - context: Context of the message
                  - inputType: Type of input
                  - table: Whether the content contains tabular data
                  - graph: Whether the content contains graph data
                  - map: Whether the content contains map data
                  - sensitive: Whether the content contains sensitive information
                  - has_specialized_terminology: Whether the content contains specialized terms
                  - scores: Intent category scores
            
        Raises:
            RoutingException: If validation fails or server returns an error
            
        Example:
            ```python
            layout = layout_controller.generate_layout(
                message="Can you create a table comparing different programming languages?",
                routing_result={
                    "suggested_template": "dashboard",
                    "content_analysis": {
                        "contentTypes": ["table", "comparison"],
                        "complexity": "medium"
                    }
                }
            )
            print(f"Generated layout template: {layout['layout']['template']}")
            print(f"Layout type: {layout['layout']['type']}")
            print(f"Components: {len(layout['layout']['components'])}")
            print(f"Content analysis: {layout['layout']['content_analysis']}")
            ```
        """
        # Validate input data
        if not message:
            raise RoutingException("Message cannot be empty")
        
        if not isinstance(message, str):
            raise RoutingException("Message must be a string")
        
        if routing_result is not None and not isinstance(routing_result, dict):
            raise RoutingException("Routing result must be a dictionary")
        
        # Use test endpoint for layout generation
        endpoint = f"{self.client.base_url}/api/routing/test/layout"
        
        payload = {
            "message": message
        }
        
        if routing_result:
            payload["routing_result"] = routing_result
            
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
            raise RoutingException(f"Failed to generate layout: {e}")
