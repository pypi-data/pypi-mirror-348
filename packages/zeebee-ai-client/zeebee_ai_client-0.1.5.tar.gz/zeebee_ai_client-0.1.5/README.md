# ZeebeeAI Python SDK

A powerful Python client for interacting with the ZeebeeAI Chat SDK Platform. This SDK provides access to all platform features including text chat, voice streaming, agent orchestration, and autonomous routing.

## Features

- **Multi-Model Chat**: Access GPT-4o, Claude-3.5 Sonnet, Grok-2, Qwen, and other models through a unified API
- **Voice Streaming**: Real-time bidirectional voice chat with WebSocket support
- **Agent Orchestration**: Create and manage AI agent pipelines for complex tasks
- **Autonomous Routing**: Intelligent routing of user queries to specialized agents
- **Semantic Search**: Integration with vector database for knowledge retrieval
- **Conversation Management**: Tools for handling conversation history and context
- **Type Hints**: Full type annotations for Python 3.10+ and mypy compatibility

## Installation

```bash
pip install zeebee-ai-client
```

## Basic Usage

```python
from zeebee_ai_client import ZeebeeClient

# Initialize with your API key
client = ZeebeeClient(api_key="YOUR_API_KEY")

# Send a chat message
def send_message():
    try:
        response = client.chat(
            message="Tell me about artificial intelligence",
            model="gpt-4o"  # Optional, default is 'gpt-4o'
        )
        
        print(f"AI response: {response['response']}")
        print(f"Conversation ID: {response['conversation_id']}")
        return response
    except Exception as e:
        print(f"Error: {e}")

# Stream chat responses
def stream_chat():
    try:
        # Enable streaming
        for chunk in client.chat(
            message="Write a short story about a robot",
            model="claude-3-5-sonnet",
            stream=True,
        ):
            # Print each chunk as it arrives
            if "text" in chunk:
                print(chunk["text"], end="", flush=True)
            
    except Exception as e:
        print(f"Error: {e}")
```

## Voice Chat

```python
import asyncio

async def voice_chat_example():
    try:
        # Voice chat with file input
        result = await client.voice_chat(
            audio_source="path/to/your/audio.webm",
            model="gpt-4o",
            # Optional handler for streaming response
            stream_handler=lambda chunk: print(f"Received chunk: {len(chunk)} bytes") 
        )
        
        print(f"Transcribed text: {result['text']}")
        print(f"Conversation ID: {result['conversation_id']}")
        
        # Save the audio response to a file
        with open("response.webm", "wb") as f:
            f.write(result["audio"])
            
    except Exception as e:
        print(f"Error in voice chat: {e}")

# Run the async function
asyncio.run(voice_chat_example())
```

## Agent Orchestration

```python
from zeebee_ai_client import ZeebeeClient, AgentController, PipelineController

# Initialize client and controllers
client = ZeebeeClient(api_key="YOUR_API_KEY")
agent_controller = AgentController(client)
pipeline_controller = PipelineController(client)

async def create_and_run_pipeline():
    try:
        # Create specialized agents
        data_cleaner = agent_controller.create_agent(
            name="Data Cleaner",
            type="data_processor",
            config={
                "cleansingOptions": {
                    "removeDuplicates": True,
                    "handleMissingValues": "imputation"
                }
            }
        )
        
        data_analyzer = agent_controller.create_agent(
            name="Data Analyzer",
            type="text_analyzer",
            config={
                "analysisType": "financial",
                "metrics": ["growth", "trends", "anomalies"]
            }
        )
        
        # Create a pipeline
        pipeline = pipeline_controller.create_pipeline(
            name="Data Analysis Pipeline",
            description="Analyzes financial data",
            stages=[
                {
                    "name": "Data Cleaning",
                    "agent_id": data_cleaner["id"]
                },
                {
                    "name": "Data Analysis",
                    "agent_id": data_analyzer["id"]
                }
            ]
        )
        
        # Execute the pipeline
        execution = pipeline_controller.execute_pipeline(
            pipeline_id=pipeline["id"],
            input_data={
                "data": "Your raw data here",
                "options": {"thoroughness": "high"}
            }
        )
        
        # Monitor execution progress
        async for update in pipeline_controller.listen_to_execution(execution["id"]):
            print(f"Status: {update['status']}")
            
            if update.get("is_complete", False):
                print(f"Final result: {update['result']}")
                break
                
    except Exception as e:
        print(f"Error: {e}")

# Run the async function
asyncio.run(create_and_run_pipeline())
```

## Error Handling

The SDK includes custom exceptions for different error types:

```python
from zeebee_ai_client import (
    AuthenticationError, 
    RateLimitError, 
    AgentException, 
    PipelineException
)

try:
    response = client.chat(message="Hello")
except AuthenticationError as e:
    print(f"Authentication error: {e}")
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
except AgentException as e:
    print(f"Agent error: {e}")
except PipelineException as e:
    print(f"Pipeline error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Example Applications

The SDK includes example applications that demonstrate its capabilities:

- **Multi-Agent Assistant**: A complex assistant that uses multiple specialized agents
- **Voice Transcription Service**: A service that transcribes speech to text
- **Interactive Voice Chat**: A voice-based chat interface

## Python Compatibility

The SDK requires Python 3.10 or newer and is fully compatible with:
- asyncio for asynchronous programming
- Type hints for static type checking
- Context managers for resource management

## Documentation

For more detailed information, see the following documentation:

- [Getting Started](./docs/GETTING_STARTED.md)
- [API Reference](./docs/API_REFERENCE.md)
- [Voice Streaming](./docs/VOICE_STREAMING.md)
- [Agent Orchestration](./docs/AGENT_ORCHESTRATION.md)

## Development

To contribute to the SDK development:

1. Clone the repository
2. Install dependencies: `pip install -e ".[dev]"`
3. Run tests: `pytest`
4. Check types: `mypy zeebee_ai_client`

## License

This SDK is licensed under the MIT License.