"""
WebSocket-based voice chat implementation for Zeebee AI client.

This module handles real-time audio streaming via WebSockets, providing
a more interactive voice chat experience compared to the standard voice_chat method.
"""

import asyncio
import json
import logging
import base64
import time
from typing import Dict, Any, Optional, Callable, Union, List
import websockets
import uuid

logger = logging.getLogger(__name__)

class VoiceChatSession:
    """
    Manages a real-time voice chat session over WebSockets.
    """
    
    def __init__(
        self,
        api_key: str,
        ws_url: str = "wss://zeebee.ai/ws",
        user_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        model: str = "gpt-4o",
        stt_provider: str = "openai",
        tts_provider: str = "openai",
        language_code: str = "en-US",
        voice_id: Optional[str] = None,
        on_transcript: Optional[Callable[[str], None]] = None,
        on_response: Optional[Callable[[str], None]] = None,
        on_audio: Optional[Callable[[bytes], None]] = None,
        on_error: Optional[Callable[[str], None]] = None,
        on_status: Optional[Callable[[str], None]] = None,
        debug: bool = False
    ):
        """
        Initialize a voice chat session.
        
        Args:
            ws_url: WebSocket server URL
            user_id: Optional user ID for tracking
            conversation_id: Optional conversation ID for continuing a chat
            model: Language model to use (e.g., "gpt-4o")
            stt_provider: Speech-to-text provider (e.g., "openai")
            tts_provider: Text-to-speech provider (e.g., "openai")
            language_code: Language code (e.g., "en-US")
            voice_id: Optional voice ID for text-to-speech
            on_transcript: Callback for transcript events
            on_response: Callback for AI response events
            on_audio: Callback for audio data events
            on_error: Callback for error events
            on_status: Callback for status updates
            debug: Enable debug logging
        """
        self.api_key = api_key
        self.ws_url = ws_url
        self.user_id = user_id or str(uuid.uuid4())
        self.conversation_id = conversation_id
        self.model = model
        self.stt_provider = stt_provider
        self.tts_provider = tts_provider
        self.language_code = language_code
        self.voice_id = voice_id
        
        # Callbacks
        self.on_transcript = on_transcript
        self.on_response = on_response
        self.on_audio = on_audio
        self.on_error = on_error
        self.on_status = on_status
        
        # State
        self.websocket = None
        self.connected = False
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
        self.heartbeat_task = None
        self.connection_task = None
        self.last_activity = time.time()
        self.is_session_active = False
        self.audio_chunks = []
        self.client_id = str(uuid.uuid4())
        
        # Debug
        self.debug = debug
        if debug:
            logging.basicConfig(level=logging.DEBUG)
            
    async def connect(self) -> bool:
        """
        Connect to the WebSocket server.
        
        Returns:
            True if connection established, False otherwise
        """
        if self.connected:
            return True
            
        try:
            if self.debug:
                logger.debug(f"Connecting to WebSocket at {self.ws_url}")
                
            if self.on_status:
                self.on_status("connecting")
                
            self.websocket = await websockets.connect(self.ws_url)
            self.connected = True
            self.is_session_active = True
            self.last_activity = time.time()
            
            if self.debug:
                logger.debug("WebSocket connection established")
                
            if self.on_status:
                self.on_status("connected")
                
            # Start heartbeat task
            self.heartbeat_task = asyncio.create_task(self._heartbeat())
            
            # Send initialization message
            init_message = {
                "type": "init",
                "api_key": self.api_key,
                "user_id": self.user_id,
                "conversation_id": self.conversation_id,
                "model": self.model,
                "client_info": {
                    "client_id": self.client_id,
                    "sdk": "python",
                }
            }
            
            await self.websocket.send(json.dumps(init_message))
            
            # Start message handler
            self.connection_task = asyncio.create_task(self._message_handler())
            
            return True
            
        except Exception as e:
            if self.debug:
                logger.error(f"WebSocket connection error: {e}")
                
            self.connected = False
            
            if self.on_error:
                self.on_error(f"Connection failed: {str(e)}")
                
            if self.on_status:
                self.on_status("disconnected")
                
            return False
    
    async def disconnect(self):
        """Disconnect from the WebSocket server."""
        self.is_session_active = False
        
        # Cancel background tasks
        if self.heartbeat_task and not self.heartbeat_task.done():
            self.heartbeat_task.cancel()
            try:
                await self.heartbeat_task
            except asyncio.CancelledError:
                pass
                
        if self.connection_task and not self.connection_task.done():
            self.connection_task.cancel()
            try:
                await self.connection_task
            except asyncio.CancelledError:
                pass
                
        # Close WebSocket connection
        if self.websocket and self.connected:
            try:
                await self.websocket.close()
            except Exception as e:
                if self.debug:
                    logger.error(f"Error closing WebSocket: {e}")
        
        self.connected = False
        if self.on_status:
            self.on_status("disconnected")
    
    async def _heartbeat(self):
        """Send periodic heartbeats to keep the connection alive."""
        try:
            while self.is_session_active and self.websocket and self.connected:
                # Send ping every 20 seconds to prevent connection timeouts
                if (time.time() - self.last_activity) > 20:
                    try:
                        ping_message = {
                            "type": "ping",
                            "timestamp": time.time(),
                            "client_id": self.client_id
                        }
                        await self.websocket.send(json.dumps(ping_message))
                        if self.debug:
                            logger.debug("Sent heartbeat ping")
                    except Exception as e:
                        if self.debug:
                            logger.error(f"Failed to send heartbeat: {e}")
                        break
                        
                await asyncio.sleep(5)
                
        except asyncio.CancelledError:
            # Task was cancelled, just exit
            pass
        except Exception as e:
            if self.debug:
                logger.error(f"Heartbeat error: {e}")
                
            if self.on_error:
                self.on_error(f"Connection error: {str(e)}")
                
            # Try to reconnect
            await self.try_reconnect()
    
    async def try_reconnect(self):
        """Attempt to reconnect to the WebSocket server."""
        if not self.is_session_active:
            return False
            
        self.connected = False
        self.reconnect_attempts += 1
        
        if self.on_status:
            self.on_status("reconnecting")
            
        if self.reconnect_attempts <= self.max_reconnect_attempts:
            if self.debug:
                logger.info(f"Attempting to reconnect (attempt {self.reconnect_attempts}/{self.max_reconnect_attempts})")
                
            # Exponential backoff for retries
            delay = min(2 ** self.reconnect_attempts, 30)
            await asyncio.sleep(delay)
            
            try:
                return await self.connect()
            except Exception as e:
                if self.debug:
                    logger.error(f"Reconnection attempt failed: {e}")
                return False
        else:
            if self.debug:
                logger.error("Maximum reconnection attempts reached")
                
            if self.on_error:
                self.on_error("Maximum reconnection attempts reached. Please try again later.")
                
            return False
    
    async def _message_handler(self):
        """Handle messages from the WebSocket connection."""
        try:
            async for message in self.websocket:
                self.last_activity = time.time()
                
                # Handle binary data (audio)
                if isinstance(message, bytes):
                    if self.on_audio:
                        await self._handle_audio_message(message)
                    continue
                
                try:
                    data = json.loads(message)
                    
                    if self.debug:
                        logger.debug(f"Received message: {data.get('type', 'unknown')}")
                    
                    message_type = data.get("type", "")
                    
                    if message_type == "pong":
                        # Heartbeat response, nothing to do
                        continue
                        
                    elif message_type == "init_ack":
                        # Connection initialized
                        if self.debug:
                            logger.debug("Connection initialized")
                            
                        if self.on_status:
                            self.on_status("ready")
                            
                    elif message_type == "transcript" or message_type == "transcription":
                        # Transcription result
                        if self.on_transcript:
                            await self._handle_transcript(data.get("text", ""))
                            
                    elif message_type == "response" or message_type == "ai_response":
                        # AI response
                        if self.on_response:
                            await self._handle_response(data.get("text", ""), data.get("conversation_id"))
                            
                    elif message_type == "audio_stream_start":
                        # Audio stream starting
                        self.audio_chunks = []
                        
                    elif message_type == "audio_chunk":
                        # Audio chunk
                        if "data" in data:
                            chunk = base64.b64decode(data["data"])
                            self.audio_chunks.append(chunk)
                            
                    elif message_type == "audio_stream_end":
                        # Audio stream complete
                        if self.audio_chunks and self.on_audio:
                            full_audio = b''.join(self.audio_chunks)
                            await self._handle_audio_message(full_audio)
                            
                    elif message_type == "error":
                        # Error message
                        error_msg = data.get("message", "Unknown error")
                        if self.debug:
                            logger.error(f"Server error: {error_msg}")
                            
                        if self.on_error:
                            self.on_error(error_msg)
                            
                    elif message_type == "status":
                        # Status update
                        if self.on_status:
                            self.on_status(data.get("status", ""))
                            
                    elif message_type == "connection_established":
                        # Initial connection confirmation
                        if self.debug:
                            logger.debug("Connection established with server")
                            
                except json.JSONDecodeError:
                    if self.debug:
                        logger.warning(f"Invalid JSON in message: {message[:100]}")
                except Exception as e:
                    if self.debug:
                        logger.error(f"Error processing message: {e}")
                    
        except websockets.exceptions.ConnectionClosed as e:
            if self.debug:
                logger.info(f"WebSocket connection closed: {e}")
                
            if self.on_status:
                self.on_status("disconnected")
                
            self.connected = False
            
            # Try to reconnect
            if self.is_session_active:
                await self.try_reconnect()
                
        except asyncio.CancelledError:
            # Task was cancelled, just exit
            pass
        except Exception as e:
            if self.debug:
                logger.error(f"Message handler error: {e}")
                
            if self.on_error:
                self.on_error(f"Connection error: {str(e)}")
                
            self.connected = False
            
            # Try to reconnect
            if self.is_session_active:
                await self.try_reconnect()
    
    async def _handle_transcript(self, text):
        """Process transcript text."""
        if callable(self.on_transcript):
            try:
                result = self.on_transcript(text)
                if asyncio.iscoroutine(result):
                    await result
            except Exception as e:
                logger.error(f"Error in transcript callback: {e}")
    
    async def _handle_response(self, text, conversation_id=None):
        """Process AI response text."""
        # Update conversation ID if provided
        if conversation_id and not self.conversation_id:
            self.conversation_id = conversation_id
            
        if callable(self.on_response):
            try:
                result = self.on_response(text)
                if asyncio.iscoroutine(result):
                    await result
            except Exception as e:
                logger.error(f"Error in response callback: {e}")
    
    async def _handle_audio_message(self, audio_data):
        """Process audio data."""
        if callable(self.on_audio):
            try:
                result = self.on_audio(audio_data)
                if asyncio.iscoroutine(result):
                    await result
            except Exception as e:
                logger.error(f"Error in audio callback: {e}")
    
    async def send_audio(self, audio_data: Union[bytes, str]) -> bool:
        """
        Send audio data to the server.
        
        Args:
            audio_data: Audio data as bytes or base64-encoded string or path to audio file
            
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.connected or not self.websocket:
            if self.debug:
                logger.error("Cannot send audio: not connected")
                
            if self.on_error:
                self.on_error("Not connected to server")
                
            return False
            
        try:
            # Handle file path
            if isinstance(audio_data, str) and not audio_data.startswith(('data:', 'http')):
                import os
                if os.path.isfile(audio_data):
                    with open(audio_data, 'rb') as f:
                        audio_data = f.read()

            # Convert to base64 if not already
            audio_base64 = audio_data
            if isinstance(audio_data, bytes):
                audio_base64 = base64.b64encode(audio_data).decode("utf-8")
                
            # Prepare message
            message = {
                "type": "audio",
                "audio_data": audio_base64,
                "conversation_id": self.conversation_id,
                "user_id": self.user_id,
                "model": self.model,
                "stt_provider": self.stt_provider,
                "tts_provider": self.tts_provider,
                "language_code": self.language_code
            }
            
            # Add voice_id if specified
            if self.voice_id:
                message["tts_voice"] = self.voice_id
                
            if self.debug:
                logger.debug("Sending audio data")
                
            await self.websocket.send(json.dumps(message))
            self.last_activity = time.time()
            
            if self.on_status:
                self.on_status("processing")
                
            return True
            
        except Exception as e:
            if self.debug:
                logger.error(f"Error sending audio: {e}")
                
            if self.on_error:
                self.on_error(f"Failed to send audio: {str(e)}")
                
            return False


class WebSocketVoiceChat:
    """
    WebSocket-based voice chat client for the Zeebee AI Platform.
    """
    
    def __init__(
        self,
        api_key: str,
        ws_url: str = "wss://zeebee.ai/ws",
        user_id: Optional[str] = None,
        debug: bool = False
    ):
        """
        Initialize the WebSocket voice chat client.
        
        Args:
            api_key: API key for authentication
            ws_url: WebSocket server URL
            user_id: Optional user ID for tracking
            debug: Enable debug logging
        """
        self.ws_url = ws_url
        self.api_key = api_key
        self.user_id = user_id or str(uuid.uuid4())
        self.debug = debug
        self.active_sessions = {}
        
        if self.debug:
            logging.basicConfig(level=logging.DEBUG)
    
    def create_session(
        self,
        conversation_id: Optional[str] = None,
        model: str = "gpt-4o",
        stt_provider: str = "openai",
        tts_provider: str = "openai",
        language_code: str = "en-US",
        voice_id: Optional[str] = None,
        on_transcript: Optional[Callable[[str], None]] = None,
        on_response: Optional[Callable[[str], None]] = None,
        on_audio: Optional[Callable[[bytes], None]] = None,
        on_error: Optional[Callable[[str], None]] = None,
        on_status: Optional[Callable[[str], None]] = None
    ) -> VoiceChatSession:
        """
        Create a new voice chat session.
        
        Args:
            conversation_id: Optional conversation ID for continuing a chat
            model: Language model to use (e.g., "gpt-4o")
            stt_provider: Speech-to-text provider (e.g., "openai")
            tts_provider: Text-to-speech provider (e.g., "openai")
            language_code: Language code (e.g., "en-US")
            voice_id: Optional voice ID for text-to-speech
            on_transcript: Callback for transcript events
            on_response: Callback for AI response events
            on_audio: Callback for audio data events
            on_error: Callback for error events
            on_status: Callback for status updates
            
        Returns:
            A new VoiceChatSession object
        """

        session = VoiceChatSession(
            ws_url=self.ws_url,
            api_key=self.api_key,
            user_id=self.user_id,
            conversation_id=conversation_id,
            model=model,
            stt_provider=stt_provider,
            tts_provider=tts_provider,
            language_code=language_code,
            voice_id=voice_id,
            on_transcript=on_transcript,
            on_response=on_response,
            on_audio=on_audio,
            on_error=on_error,
            on_status=on_status,
            debug=self.debug
        )
        
        # Store the session
        session_id = str(uuid.uuid4())
        self.active_sessions[session_id] = session
        
        return session
    
    async def close_all_sessions(self):
        """Close all active sessions."""
        for session_id, session in list(self.active_sessions.items()):
            try:
                await session.disconnect()
            except Exception as e:
                if self.debug:
                    logger.error(f"Error closing session {session_id}: {e}")
                    
        self.active_sessions.clear()
    
    def get_active_sessions(self) -> List[VoiceChatSession]:
        """Get all active sessions."""
        return list(self.active_sessions.values())
    
    def get_session_count(self) -> int:
        """Get the number of active sessions."""
        return len(self.active_sessions)
