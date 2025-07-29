"""
Python Client SDK for Zeebee AI Chat Platform.

This module provides a simple client for interacting with the Zeebee AI Chat API.
It supports:
- Text chat
- Voice chat via WebSocket
- Session management
- Response formatting
"""

import json
import requests
import time
import uuid
import logging
import os
from typing import Dict, List, Any, Optional, Union, Generator, Callable
import asyncio
import websockets

from .exceptions import AuthenticationError, RateLimitError
from .agents import AgentController
from .pipelines import PipelineController
from .routing import RoutingController
from .voice_chat import WebSocketVoiceChat, VoiceChatSession

logger = logging.getLogger(__name__)

class ZeebeeClient:
    """
    Client for the Zeebee AI Chat Platform.
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://zeebee.ai",
        ws_url: str = "wss://zeebee.ai/ws",
        version: str = "v1",
        timeout: int = 60,
        debug: bool = False
    ):
        """
        Initialize the Zeebee client.
        
        Args:
            api_key: API key for authentication
            base_url: Base URL for the API
            version: API version
            timeout: Request timeout in seconds
            debug: Enable debug logging
        """
        # Initialize session first to ensure it's available to other components
        self._session = requests.Session()
        
        self.api_key = api_key
        self.base_url = base_url
        self.version = version
        self.timeout = timeout
        
        # Initialize other attributes
        self.session_id = str(uuid.uuid4())
        self.conversations = {}
        
        # Configure logging
        self.debug = debug
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        
        # Validate API key
        if not self.api_key:
            logger.warning("No API key provided. Some functionality may be limited.")
            
        # Initialize controllers after session is created
        self.agents = AgentController(self)
        self.pipelines = PipelineController(self)
        self.routing = RoutingController(self)
        
        # Initialize WebSocket voice chat client
        self.ws_voice_chat = WebSocketVoiceChat(
            ws_url=ws_url,
            api_key=self.api_key,
            user_id=self.session_id,
            debug=debug
        )
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": f"zeebee-python-sdk/{self.version}",
            "X-Session-ID": self.session_id
        }
        
        if self.api_key:
            headers["X-API-Key"] = self.api_key

        return headers
    
    def _handle_error_response(self, response: requests.Response) -> None:
        """Handle error responses from the API."""
        try:
            error_data = response.json()
        except ValueError:
            error_data = {"error": response.text}
            
        error_message = error_data.get("error", "Unknown error")
        
        if response.status_code == 401:
            raise AuthenticationError(f"Authentication failed: {error_message}")
        elif response.status_code == 429:
            raise RateLimitError(f"Rate limit exceeded: {error_message}")
        else:
            response.raise_for_status()
    
    def chat(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        model: str = "gpt-4o",
        system_prompt: Optional[str] = None,
        template_name: Optional[str] = None,
        template_variables: Optional[Dict[str, Any]] = None,
        stream: bool = False,
        layout: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: float = 0.7,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        stop_sequences: Optional[List[str]] = None,
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Union[Dict[str, Any], Generator[Dict[str, Any], None, None]]:
        """
        Send a message to the chat API.
        
        Args:
            message: User message
            conversation_id: Optional ID for continuing a conversation
            model: LLM model to use
            system_prompt: Optional system prompt
            template_name: Optional template name
            template_variables: Optional template variables
            stream: Whether to stream the response
            layout: Response layout name
            max_tokens: Maximum tokens in the response
            temperature: Temperature for sampling (0-1)
            top_p: Top-p sampling parameter (0-1)
            frequency_penalty: Frequency penalty (0-2)
            presence_penalty: Presence penalty (0-2)
            stop_sequences: Optional list of stop sequences
            user_id: Optional user identifier
            metadata: Optional additional metadata
            
        Returns:
            Response as dict or generator of response chunks
        """
        endpoint = f"https://api.zeebee.ai/api/chat/completions"
        
        # Prepare message object
        messages = [{"role": "user", "content": message}]
        
        payload = {
            "messages": messages,
            "model": model,
            "stream": stream,
            "conversation_id": conversation_id,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty
        }
        
        # Add optional parameters
        if system_prompt:
            messages.insert(0, {"role": "system", "content": system_prompt})
            
        if template_name:
            payload["template"] = {
                "name": template_name,
                "variables": template_variables or {}
            }
            
        if layout:
            payload["layout"] = layout
            
        if stop_sequences:
            payload["stop"] = stop_sequences
            
        if user_id:
            payload["user_id"] = user_id
            
        if metadata:
            payload["metadata"] = metadata
        
        if stream:
            return self._stream_chat(endpoint, payload)
        else:
            return self._send_chat(endpoint, payload)
    
    def _send_chat(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send a chat request."""
        try:
            response = self._session.post(
                endpoint,
                headers=self._get_headers(),
                json=payload,
                timeout=self.timeout
            )
            
            self._handle_error_response(response)
            
            result = response.json()
            
            # Store conversation ID
            if result.get("conversation_id"):
                self.conversations[result["conversation_id"]] = {
                    "model": payload.get("model"),
                    "last_message": payload.get("messages", [{}])[-1].get("content"),
                    "updated_at": time.time()
                }
                
            return result
            
        except requests.RequestException as e:
            logger.error(f"Chat request failed: {e}")
            raise
    
    def _stream_chat(self, endpoint: str, payload: Dict[str, Any]) -> Generator[Dict[str, Any], None, None]:
        """Stream a chat response."""
        try:
            with self._session.post(
                endpoint,
                headers=self._get_headers(),
                json=payload,
                timeout=self.timeout,
                stream=True
            ) as response:
                self._handle_error_response(response)
                
                # Process the streamed response
                conversation_id = None
                
                for line in response.iter_lines():
                    if not line:
                        continue
                        
                    try:
                        line_text = line.decode('utf-8')
                        # Skip [DONE] markers
                        if line_text == "data: [DONE]":
                            continue
                        
                        # Parse the JSON chunk
                        if line_text.startswith("data: "):
                            chunk = json.loads(line_text.lstrip('data: '))
                        
                            # Store conversation ID
                            if chunk.get("conversation_id") and not conversation_id:
                                conversation_id = chunk["conversation_id"]
                                self.conversations[conversation_id] = {
                                    "model": payload.get("model"),
                                    "last_message": payload.get("messages", [{}])[-1].get("content"),
                                    "updated_at": time.time()
                                }
                                
                            yield chunk
                        
                    except json.JSONDecodeError:
                        logger.warning(f"Invalid JSON in stream: {line}")
                    
        except requests.RequestException as e:
            logger.error(f"Chat stream request failed: {e}")
            raise
    
    async def voice_chat(
        self,
        audio_source: Union[str, bytes],
        conversation_id: Optional[str] = None,
        model: str = "gpt-4o",
        stt_model: str = "whisper",
        tts_model: str = "openai_tts",
        language_code: str = "en-US",
        voice_id: str = "default",
        stream_handler: Optional[Callable[[Union[str, bytes]], None]] = None,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send a voice message and receive a voice response.
        
        Args:
            audio_source: Path to audio file or audio bytes
            conversation_id: Optional ID for continuing a conversation
            model: LLM model to use
            stt_model: Speech-to-text model
            tts_model: Text-to-speech model
            language_code: Language code (e.g., "en-US")
            voice_id: Voice identifier
            stream_handler: Optional handler for streaming response chunks
            user_id: Optional user identifier
            
        Returns:
            Response metadata
        """
        # First create a streaming session
        stream_request = {
            "user_id": user_id,
            "model": model,
            "conversation_id": conversation_id,
            "stt_model": stt_model,
            "tts_model": tts_model,
            "voice_id": voice_id,
            "language_code": language_code
        }
        
        # Create the session
        create_session_endpoint = f"{self.base_url}/api/voice/stream"
        response = requests.post(
            create_session_endpoint,
            headers=self._get_headers(),
            json=stream_request,
            timeout=self.timeout
        )
        self._handle_error_response(response)
        
        session_data = response.json()
        session_id = session_data.get("session_id")
        session_token = session_data.get("token")
        
        if not session_id or not session_token:
            raise ValueError("Failed to create voice streaming session")
        
        # Prepare WebSocket URL
        ws_url = f"{self.base_url.replace('http', 'ws')}/voice/stream/{session_id}"
        
        # Read audio file if a path was provided
        if isinstance(audio_source, str):
            with open(audio_source, 'rb') as f:
                audio_data = f.read()
        else:
            audio_data = audio_source
        
        # Connect to WebSocket
        websocket_headers = {
            "Authorization": f"Bearer {session_token}"
        }
        
        async with websockets.connect(ws_url, extra_headers=websocket_headers) as ws:
            # Send initial authentication message
            auth_message = {
                "token": session_token,
                "config": {
                    "sample_rate": 16000,
                    "channels": 1,
                    "encoding": "LINEAR16",
                },
                "stt_model": stt_model,
                "tts_model": tts_model,
                "voice_id": voice_id,
                "language_code": language_code
            }
            await ws.send(json.dumps(auth_message))
            
            # Send audio data
            await ws.send(audio_data)
            
            # Signal end of audio
            await ws.send(json.dumps({"type": "end_of_audio"}))
            
            # Process response
            response_chunks = []
            response_text = ""
            transcription = ""
            
            while True:
                message = await ws.recv()
                
                # Handle binary audio data
                if isinstance(message, bytes):
                    response_chunks.append(message)
                    if stream_handler:
                        await stream_handler(message)
                    continue
                
                # Handle JSON metadata
                try:
                    data = json.loads(message)
                    message_type = data.get("type", "")
                    
                    if message_type == "transcription":
                        # Store transcription
                        transcription = data.get("text", "")
                        logger.info(f"Transcription: {transcription}")
                        
                    elif message_type == "ai_response":
                        # Store AI response text
                        response_text = data.get("text", "")
                        logger.info(f"AI response: {response_text}")
                        
                    elif message_type == "speech":
                        # Handle speech data (in binary format above)
                        pass
                        
                    elif message_type == "error":
                        # Handle error
                        error_message = data.get("message", "Unknown error")
                        logger.error(f"WebSocket error: {error_message}")
                        
                    elif message_type == "session_ended" or message_type == "end_of_response":
                        # End of session
                        break
                        
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON in WebSocket message: {message}")
            
            # Combine all audio chunks
            full_audio = b''.join(response_chunks)
            
            # End the session gracefully
            try:
                end_session_endpoint = f"{self.base_url}/api/voice/stream/{session_id}/end"
                requests.post(
                    end_session_endpoint,
                    headers={"Authorization": f"Bearer {session_token}"},
                    timeout=self.timeout
                )
            except Exception as e:
                logger.warning(f"Error ending session: {e}")
            
            return {
                "conversation_id": conversation_id,
                "session_id": session_id,
                "text": response_text,
                "transcription": transcription,
                "audio": full_audio,
                "model": model
            }
    
    def speech_to_text(
        self,
        audio_source: Union[str, bytes],
        language: Optional[str] = None,
        provider: str = "openai",
        model: str = "whisper"
    ) -> Dict[str, Any]:
        """
        Convert speech to text.
        
        Args:
            audio_source: Path to audio file or audio bytes
            language: Optional language code
            provider: Speech-to-text provider
            model: STT model to use
            
        Returns:
            Transcription result
        """
        endpoint = f"{self.base_url}/api/voice/stt"
        
        # Read audio file if a path was provided
        if isinstance(audio_source, str):
            with open(audio_source, 'rb') as f:
                audio_data = f.read()
        else:
            audio_data = audio_source
        
        # Convert audio to base64 for API request
        import base64
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        # Create request payload
        data = {
            "audio": audio_base64,
            "config": {
                "encoding": "LINEAR16",
                "sample_rate": 16000,
                "channels": 1,
                "language_code": language or "en-US"
            },
            "model": model
        }
        
        # Send the request
        try:
            response = requests.post(
                endpoint,
                headers=self._get_headers(),
                json=data,
                timeout=self.timeout
            )
            
            self._handle_error_response(response)
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Speech-to-text request failed: {e}")
            raise
    
    def text_to_speech(
        self,
        text: str,
        voice_id: str = "default",
        language_code: str = "en-US",
        model: str = "openai_tts"
    ) -> Dict[str, Any]:
        """
        Convert text to speech.
        
        Args:
            text: Text to convert to speech
            voice_id: Voice identifier
            language_code: Language code
            model: TTS model to use
            
        Returns:
            Speech synthesis result
        """
        endpoint = f"{self.base_url}/api/voice/tts"
        
        data = {
            "text": text,
            "voice_id": voice_id,
            "language_code": language_code,
            "model": model
        }
        
        try:
            response = requests.post(
                endpoint,
                headers=self._get_headers(),
                json=data,
                timeout=self.timeout
            )
            
            self._handle_error_response(response)
            result = response.json()
            
            # The result includes base64-encoded audio that we can decode
            if "audio" in result:
                import base64
                result["audio_bytes"] = base64.b64decode(result["audio"])
                
            return result
            
        except requests.RequestException as e:
            logger.error(f"Text-to-speech request failed: {e}")
            raise
    
    def get_conversation(
        self, 
        conversation_id: str
    ) -> Dict[str, Any]:
        """
        Get conversation details.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            Conversation details
        """
        endpoint = f"https://api.zeebee.ai/api/conversations/{conversation_id}"
        
        try:
            response = requests.get(
                endpoint,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            self._handle_error_response(response)
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Get conversation request failed: {e}")
            raise
    
    def list_conversations(
        self,
        limit: int = 20,
        offset: int = 0,
        status: str = "active",
        order: str = "desc"
    ) -> Dict[str, Any]:
        """
        List conversations.
        
        Args:
            limit: Maximum number of conversations to return
            offset: Pagination offset
            status: Filter by status (active/archived/all)
            order: Sort order (desc/asc)
            
        Returns:
            List of conversations
        """
        endpoint = f"https://api.zeebee.ai/api/conversations"
        
        try:
            response = requests.get(
                endpoint,
                headers=self._get_headers(),
                params={
                    "limit": limit, 
                    "offset": offset,
                    "status": status,
                    "order": order
                },
                timeout=self.timeout
            )
            
            self._handle_error_response(response)
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"List conversations request failed: {e}")
            raise
    
    def create_conversation(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new conversation.
        
        Args:
            title: Optional conversation title
            description: Optional conversation description
            model: Optional default model
            system_prompt: Optional system prompt
            metadata: Optional additional metadata
            
        Returns:
            Created conversation
        """
        endpoint = f"https://api.zeebee.ai/api/conversations"
        
        data = {
            "title": title,
            "description": description,
            "model": model,
            "system_prompt": system_prompt,
            "metadata": metadata or {}
        }
        
        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}
        
        try:
            response = requests.post(
                endpoint,
                headers=self._get_headers(),
                json=data,
                timeout=self.timeout
            )
            
            self._handle_error_response(response)
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Create conversation request failed: {e}")
            raise
    
    def update_conversation(
        self,
        conversation_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        model: Optional[str] = None,
        system_prompt: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Update a conversation.
        
        Args:
            conversation_id: Conversation ID
            title: Optional new title
            description: Optional new description
            model: Optional new default model
            system_prompt: Optional new system prompt
            metadata: Optional new metadata
            
        Returns:
            Updated conversation
        """
        endpoint = f"https://api.zeebee.ai/api/conversations/{conversation_id}"
        
        data = {
            "title": title,
            "description": description,
            "model": model,
            "system_prompt": system_prompt,
            "metadata": metadata
        }
        
        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}
        
        try:
            response = requests.patch(
                endpoint,
                headers=self._get_headers(),
                json=data,
                timeout=self.timeout
            )
            
            self._handle_error_response(response)
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Update conversation request failed: {e}")
            raise
    
    def delete_conversation(
        self,
        conversation_id: str
    ) -> Dict[str, Any]:
        """
        Delete a conversation.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            Deletion confirmation
        """
        endpoint = f"https://api.zeebee.ai/api/conversations/{conversation_id}"

        try:
            response = requests.delete(
                endpoint,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            self._handle_error_response(response)
            
            # Remove from local cache
            if conversation_id in self.conversations:
                del self.conversations[conversation_id]
                
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Delete conversation request failed: {e}")
            raise
    
    def archive_conversation(
        self,
        conversation_id: str
    ) -> Dict[str, Any]:
        """
        Archive a conversation.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            Updated conversation
        """
        endpoint = f"https://api.zeebee.ai/api/conversations/{conversation_id}/archive"
        
        try:
            response = requests.post(
                endpoint,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            self._handle_error_response(response)
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Archive conversation request failed: {e}")
            raise
    
    def restore_conversation(
        self,
        conversation_id: str
    ) -> Dict[str, Any]:
        """
        Restore an archived conversation.
        
        Args:
            conversation_id: Conversation ID
            
        Returns:
            Updated conversation
        """
        endpoint = f"https://api.zeebee.ai/api/conversations/{conversation_id}/restore"
        
        try:
            response = requests.post(
                endpoint,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            self._handle_error_response(response)
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Restore conversation request failed: {e}")
            raise
    
    def add_message(
        self,
        conversation_id: str,
        content: str,
        role: str = "user",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Add a message to a conversation.
        
        Args:
            conversation_id: Conversation ID
            content: Message content
            role: Message role (user, assistant, system)
            metadata: Optional additional metadata
            
        Returns:
            Added message
        """
        endpoint = f"https://api.zeebee.ai/api/conversations/{conversation_id}/messages"
        
        data = {
            "role": role,
            "content": content,
            "metadata": metadata or {}
        }
        
        try:
            response = requests.post(
                endpoint,
                headers=self._get_headers(),
                json=data,
                timeout=self.timeout
            )
            
            self._handle_error_response(response)
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Add message request failed: {e}")
            raise
    
    def export_conversation(
        self,
        conversation_id: str,
        format: str = "json"
    ) -> Union[Dict[str, Any], str]:
        """
        Export a conversation.
        
        Args:
            conversation_id: Conversation ID
            format: Export format (json, markdown, text)
            
        Returns:
            Exported conversation
        """
        endpoint = f"https://api.zeebee.ai/api/conversations/{conversation_id}/export"
        
        try:
            response = requests.get(
                endpoint,
                headers=self._get_headers(),
                params={"format": format},
                timeout=self.timeout
            )
            
            self._handle_error_response(response)
            
            # Return appropriate format
            if format == "json":
                return response.json()
            else:
                return response.text
            
        except requests.RequestException as e:
            logger.error(f"Export conversation request failed: {e}")
            raise
    
    def search_messages(
        self,
        query: str,
        conversation_id: str,
        limit: int = 10,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search for messages in a conversation.
        
        Args:
            query: Search query
            conversation_id: Conversation ID
            limit: Maximum number of results to return
            offset: Pagination offset
            
        Returns:
            Search results
        """
        endpoint = f"https://api.zeebee.ai/api/conversations/{conversation_id}/search"
        
        data = {
            "query": query,
            "limit": limit,
            "offset": offset
        }
        
        try:
            response = requests.post(
                endpoint,
                headers=self._get_headers(),
                json=data,
                timeout=self.timeout
            )
            
            self._handle_error_response(response)
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Search messages request failed: {e}")
            raise
    
    def search(
        self,
        query: str,
        search_type: str = "conversations",
        limit: int = 10,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Search conversations or messages.
        
        Args:
            query: Search query
            search_type: Type of search (conversations, messages)
            limit: Maximum number of results to return
            offset: Pagination offset
            
        Returns:
            Search results
        """
        endpoint = f"{self.base_url}/api/search/{search_type}"
        
        payload = {
            "query": query,
            "limit": limit,
            "offset": offset
        }
        
        try:
            response = requests.post(
                endpoint,
                headers=self._get_headers(),
                json=payload,
                timeout=self.timeout
            )
            
            self._handle_error_response(response)
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Search request failed: {e}")
            raise
    
    def list_voice_models(
        self,
        type: str = "stt"  # "stt" or "tts"
    ) -> List[Dict[str, Any]]:
        """
        List available voice models.
        
        Args:
            type: Model type (stt, tts)
            
        Returns:
            List of available models
        """
        endpoint = f"{self.base_url}/api/voice/{type}/models"
        
        try:
            response = requests.get(
                endpoint,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            self._handle_error_response(response)
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"List voice models request failed: {e}")
            raise
    
    def list_voices(
        self,
        language_code: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List available voices.
        
        Args:
            language_code: Optional language code to filter voices
            
        Returns:
            List of available voices
        """
        endpoint = f"{self.base_url}/api/voice/voices"
        
        params = {}
        if language_code:
            params["language_code"] = language_code
        
        try:
            response = requests.get(
                endpoint,
                headers=self._get_headers(),
                params=params,
                timeout=self.timeout
            )
            
            self._handle_error_response(response)
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"List voices request failed: {e}")
            raise
    
    def get_available_agents(self) -> List[Dict[str, Any]]:
        """
        Get list of available agents.
        
        Returns:
            List of available agents
        """
        endpoint = f"{self.base_url}/api/agents"
        
        try:
            response = requests.get(
                endpoint,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            self._handle_error_response(response)
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Get available agents request failed: {e}")
            raise
    
    def get_available_layouts(self) -> List[Dict[str, Any]]:
        """
        Get list of available response layouts.
        
        Returns:
            List of available layouts
        """
        endpoint = f"{self.base_url}/api/layouts"
        
        try:
            response = requests.get(
                endpoint,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            self._handle_error_response(response)
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Get available layouts request failed: {e}")
            raise
    
    def submit_feedback(
        self,
        conversation_id: str,
        message_id: str,
        feedback_type: str,
        feedback_value: Union[int, float],
        comment: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Submit feedback for a message.
        
        Args:
            conversation_id: Conversation ID
            message_id: Message ID
            feedback_type: Type of feedback (thumbs_up, thumbs_down, rating, report)
            feedback_value: Numeric feedback value
            comment: Optional comment
            
        Returns:
            Feedback submission confirmation
        """
        endpoint = f"{self.base_url}/api/feedback"
        
        payload = {
            "conversation_id": conversation_id,
            "message_id": message_id,
            "feedback_type": feedback_type,
            "feedback_value": feedback_value
        }
        
        if comment:
            payload["comment"] = comment
            
        try:
            response = requests.post(
                endpoint,
                headers=self._get_headers(),
                json=payload,
                timeout=self.timeout
            )
            
            self._handle_error_response(response)
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Submit feedback request failed: {e}")
            raise
    
    async def voice_chat_ws(
        self,
        audio_source: Union[str, bytes],
        conversation_id: Optional[str] = None,
        model: str = "gpt-4o",
        stt_model: str = "openai",
        tts_model: str = "openai",
        language_code: str = "en-US",
        voice_id: str = "alloy",
        block: bool = True,
        timeout: int = 60,
        callbacks: Optional[Dict[str, Callable]] = None
    ) -> Dict[str, Any]:
        """
        Send a voice message and receive a voice response using WebSockets.
        
        Args:
            audio_source: Path to audio file or audio bytes
            conversation_id: Optional ID for continuing a conversation
            model: LLM model to use
            stt_model: Speech-to-text model provider
            tts_model: Text-to-speech model provider
            language_code: Language code (e.g., "en-US")
            voice_id: Voice identifier
            block: Whether to block until response is complete
            timeout: Timeout in seconds for waiting for response
            callbacks: Optional callbacks for events:
                - on_transcript: Called when transcript is received
                - on_response: Called when AI response is received
                - on_audio: Called when audio response is received
                - on_error: Called when an error occurs
                - on_status: Called when status changes
            
        Returns:
            Response metadata including conversation_id and transcription
        """
        # Initialize callbacks dictionary if not provided
        if callbacks is None:
            callbacks = {}
            
        # Set up callbacks
        on_transcript = callbacks.get("on_transcript")
        on_response = callbacks.get("on_response")
        on_audio = callbacks.get("on_audio")
        on_error = callbacks.get("on_error")
        on_status = callbacks.get("on_status")
        
        # Results to capture
        results = {
            "transcription": None,
            "response": None,
            "audio": None,
            "conversation_id": conversation_id,
            "complete": False,
            "status": "initializing"
        }
        
        # Event for tracking completion
        completion_event = asyncio.Event()
        
        # Set up result capture callbacks
        async def capture_transcript(text):
            results["transcription"] = text
            if callable(on_transcript):
                try:
                    on_transcript(text)
                except Exception as e:
                    logger.error(f"Error in transcript callback: {e}")
                
        async def capture_response(text):
            results["response"] = text
            if callable(on_response):
                try:
                    on_response(text)
                except Exception as e:
                    logger.error(f"Error in response callback: {e}")
                
        async def capture_audio(audio_data):
            results["audio"] = audio_data
            if callable(on_audio):
                try:
                    on_audio(audio_data)
                except Exception as e:
                    logger.error(f"Error in audio callback: {e}")
                    
            # Mark as complete when we get audio
            results["complete"] = True
            completion_event.set()
                
        async def capture_error(error_msg):
            results["error"] = error_msg
            if callable(on_error):
                try:
                    on_error(error_msg)
                except Exception as e:
                    logger.error(f"Error in error callback: {e}")
                    
            # Mark as complete on error
            results["complete"] = True
            completion_event.set()
                
        async def update_status(status):
            results["status"] = status
            if callable(on_status):
                try:
                    on_status(status)
                except Exception as e:
                    logger.error(f"Error in status callback: {e}")
        
        # Create a new session
        session = self.ws_voice_chat.create_session(
            conversation_id=conversation_id,
            model=model,
            stt_provider=stt_model,
            tts_provider=tts_model,
            language_code=language_code,
            voice_id=voice_id,
            on_transcript=capture_transcript,
            on_response=capture_response,
            on_audio=capture_audio,
            on_error=capture_error,
            on_status=update_status
        )
        
        # Connect to WebSocket server
        connected = await session.connect()
        
        if not connected:
            results["error"] = "Failed to connect to voice chat server"
            results["complete"] = True
            results["status"] = "error"
            return results
        
        # Handle audio file source
        try:
            # Read audio file if a path was provided
            if isinstance(audio_source, str) and os.path.isfile(audio_source):
                with open(audio_source, 'rb') as f:
                    audio_data = f.read()
            else:
                audio_data = audio_source
                
            # Send audio data
            sent = await session.send_audio(audio_data)
            
            if not sent:
                results["error"] = "Failed to send audio data"
                results["complete"] = True
                results["status"] = "error"
                await session.disconnect()
                return results
                
        except Exception as e:
            logger.error(f"Error handling audio source: {e}")
            results["error"] = f"Error processing audio: {str(e)}"
            results["complete"] = True
            results["status"] = "error"
            await session.disconnect()
            return results
        
        if block:
            # Wait for completion with timeout
            try:
                await asyncio.wait_for(completion_event.wait(), timeout=timeout)
            except asyncio.TimeoutError:
                logger.warning(f"Timeout waiting for voice chat response after {timeout} seconds")
                results["error"] = f"Timeout waiting for response after {timeout} seconds"
                results["complete"] = True
                results["status"] = "timeout"
                
            # Close session
            await session.disconnect()
            
        # Update conversation ID if it was created
        if not conversation_id and session.conversation_id:
            results["conversation_id"] = session.conversation_id
            
        return results
    
    def create_voice_chat_session(
        self,
        conversation_id: Optional[str] = None,
        model: str = "gpt-4o",
        stt_model: str = "openai",
        tts_model: str = "openai",
        language_code: str = "en-US",
        voice_id: str = "alloy",
        callbacks: Optional[Dict[str, Callable]] = None
    ) -> VoiceChatSession:
        """
        Create an interactive voice chat session using WebSockets.
        
        Args:
            conversation_id: Optional ID for continuing a conversation
            model: LLM model to use
            stt_model: Speech-to-text model provider
            tts_model: Text-to-speech model provider
            language_code: Language code (e.g., "en-US")
            voice_id: Voice identifier
            callbacks: Optional callbacks for events:
                - on_transcript: Called when transcript is received
                - on_response: Called when AI response is received
                - on_audio: Called when audio response is received
                - on_error: Called when an error occurs
                - on_status: Called when status changes
                
        Returns:
            A voice chat session that can be used to send audio messages
        """
        # Extract callbacks
        if callbacks is None:
            callbacks = {}
            
        on_transcript = callbacks.get("on_transcript")
        on_response = callbacks.get("on_response")
        on_audio = callbacks.get("on_audio")
        on_error = callbacks.get("on_error")
        on_status = callbacks.get("on_status")
        
        # Create a new session
        session = self.ws_voice_chat.create_session(
            conversation_id=conversation_id,
            model=model,
            stt_provider=stt_model,
            tts_provider=tts_model,
            language_code=language_code,
            voice_id=voice_id,
            on_transcript=on_transcript,
            on_response=on_response,
            on_audio=on_audio,
            on_error=on_error,
            on_status=on_status
        )
        
        return session