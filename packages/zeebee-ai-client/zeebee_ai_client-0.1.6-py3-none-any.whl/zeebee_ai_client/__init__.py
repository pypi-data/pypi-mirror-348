"""
ZeebeeAI Python Client SDK

This package provides a comprehensive client for interacting with the ZeebeeAI Chat Platform.
"""

from .client import ZeebeeClient
from .exceptions import (
    AuthenticationError,
    RateLimitError,
    AgentException,
    PipelineException,
    RoutingException,
)
from .agents import AgentController, AgentTypes
from .pipelines import PipelineController
from .routing import RoutingController
from .layout import LayoutController, IntentCategory, LayoutType
from .voice_chat import VoiceChatSession, WebSocketVoiceChat

__version__ = "0.1.6"
__all__ = [
    "ZeebeeClient",
    "AgentController",
    "PipelineController",
    "RoutingController",
    "LayoutController",
    "IntentCategory",
    "LayoutType",
    "AuthenticationError",
    "RateLimitError",
    "AgentException",
    "PipelineException",
    "RoutingException",
    "AgentTypes",
    "VoiceChatSession",
    "WebSocketVoiceChat"
]
