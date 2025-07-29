# websocket_server.py
from .features import Feature, WebSearchAgent, DefaultChatFeature, FastGoogleSearch, SearchAgent
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
import uvicorn
from typing import List, Dict, Optional, Union, Any
import asyncio
from openai import OpenAI



class ModelService:
    """Handles model interactions and streaming responses"""

    def __init__(
        self,
        model_name: str = "llama3.2:latest",
        api_key: Optional[str] = "ollama",
        base_url: str = "http://0.0.0.0:11434/v1",
        temperature: float = 0.0,
        max_tokens: int = 4000,
        top_p: float = 1.0,
        stream: bool = True,
    ):
        self.model_name = model_name
        self.api_key = api_key
        self.base_url = base_url
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.stream = stream

        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )

    async def stream_response(
        self,
        websocket: WebSocket,
        message: str,
        system_prompt: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
        model: Optional[str] = None,
        **kwargs
    ):
        """Stream model responses"""
        try:
            print(f"Starting stream with model: {model or self.model_name}")
            print(f"System prompt: {system_prompt}")
            print(f"User message: {message}")

            messages = [{"role": "system", "content": system_prompt}]

            if chat_history:
                messages.extend(chat_history)

            messages.append({"role": "user", "content": message})

            stream = self.client.chat.completions.create(
                model=model or self.model_name,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                stream=self.stream
            )

            for chunk in stream:
                if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content is not None:
                    await websocket.send_text(json.dumps({
                        "sender": "bot",
                        "message": chunk.choices[0].delta.content,
                        "type": "stream"
                    }))
                    await asyncio.sleep(0.01)

            await websocket.send_text(json.dumps({
                "sender": "bot",
                "type": "end_stream"
            }))
            print("Stream completed")

        except Exception as e:
            print(f"Error in streaming: {str(e)}")
            await websocket.send_text(json.dumps({
                "sender": "bot",
                "message": f"Error: {str(e)}",
                "type": "error"
            }))



class WebSocketChatServer:
    def __init__(
        self,
        model_name: str = "llama3.2:latest",
        api_key: Optional[str] = "ollama",
        base_url: str = "http://0.0.0.0:11434/v1",
        temperature: float = 0.0,
        max_tokens: int = 4000,
        top_p: float = 1.0,
        stream: bool = True,
        host: str = "0.0.0.0",
        port: int = 8143
    ):
        self.app = FastAPI()
        self.model_name = model_name
        self.api_key = api_key
        self.base_url = base_url
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.stream = stream
        self.host = host
        self.port = port
        self.active_connections: set = set()

        # Create model service
        self.model_service = ModelService(
            model_name=model_name,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=stream
        )

        # Initialize features
        self.features = self._initialize_features()

        self.setup_routes()

    def _initialize_features(self) -> Dict[str, Feature]:
        """Initialize available features"""
        return {
            'WebSearchAgent': WebSearchAgent(self.model_service),
            'chat': DefaultChatFeature(self.model_service),
            'is_websearch_chat': FastGoogleSearch(self.model_service),
            'SearchAgent': SearchAgent(self.model_service),
        }

    def setup_routes(self):
        @self.app.websocket("/ws/{client_id}")
        async def websocket_endpoint(websocket: WebSocket, client_id: str):
            await websocket.accept()
            self.active_connections.add(websocket)
            print(f"Client {client_id} connected")

            try:
                while True:
                    data = await websocket.receive_text()
                    message_data = json.loads(data)

                    for k,v in message_data.items():
                        print(f'{k}:{v}')

                    # Extract parameters from the message
                    user_message = message_data["message"]
                    system_prompt = message_data.get("system_prompt", "You are a helpful AI assistant.")
                    app_type = message_data.get("app_type", "chat")
                    model = message_data.get("model", self.model_name)
                    is_websearch_k = message_data.get("is_websearch_k", 3)
                    agent_type = message_data.get("agent_type", None)
                    is_websearch_chat = message_data.get("is_websearch_chat", False)
                    chat_history = message_data.get("chat_history", [])
                    base_url = message_data.get("base_url", self.base_url)
                    api_key = message_data.get("api_key", self.api_key)

                    # Get the appropriate feature handler
                    if is_websearch_chat and agent_type not in ['WebSearchAgent', 'SearchAgent']:
                        feature = self.features["is_websearch_chat"]
                    elif agent_type:
                        feature = self.features.get(agent_type, self.features['chat'])
                    else:
                        feature = self.features.get(app_type, self.features['chat'])

                    # Handle the message with the selected feature
                    await feature.handle(
                        websocket=websocket,
                        message=user_message,
                        system_prompt=system_prompt,
                        chat_history=chat_history,
                        is_websearch_k=is_websearch_k,
                        base_url=base_url,
                        api_key=api_key,
                        model=model
                    )

            except WebSocketDisconnect:
                self.active_connections.remove(websocket)
                print(f"Client {client_id} disconnected")
            except Exception as e:
                if websocket in self.active_connections:
                    self.active_connections.remove(websocket)
                print(f"Error in websocket endpoint: {str(e)}")

    def run(self):
        """Start the server"""
        uvicorn.run(self.app, host=self.host, port=self.port, log_level="debug")


def create_websocket_server(
    model_name: str = "",
    api_key: Optional[str] = "ollama",
    base_url: str = "http://0.0.0.0:11434/v1",
    temperature: float = 0.0,
    max_tokens: int = 4000,
    top_p: float = 1.0,
    stream: bool = True,
    host: str = "0.0.0.0",
    port: int = 8143
):
    """Create and run a WebSocket chat server with the specified parameters"""
    server = WebSocketChatServer(
        model_name=model_name,
        api_key=api_key,
        base_url=base_url,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        stream=stream,
        host=host,
        port=port
    )
    server.run()


# Shortcut functions for commonly used models
def local_llama3(
    base_url: str = "http://0.0.0.0:11434/v1",
    model_name: str = "llama3.2:latest",
    host: str = "0.0.0.0",
    port: int = 8143,
    **kwargs
):
    return create_websocket_server(
        model_name=model_name,
        base_url=base_url,
        host=host,
        port=port,
        **kwargs
    )


def local_qwen(
    base_url: str = "http://0.0.0.0:11434/v1",
    model_name: str = "qwen2.5:7b-instruct",
    host: str = "0.0.0.0",
    port: int = 8143,
    **kwargs
):
    return create_websocket_server(
        model_name=model_name,
        base_url=base_url,
        host=host,
        port=port,
        **kwargs
    )


if __name__ == "__main__":
    # Example usage:
    local_llama3()
    # Or with custom parameters:
    # create_websocket_server(
    #     model_name="qwen2.5:7b-instruct",
    #     base_url="http://192.168.170.76:11434/v1",
    #     host="0.0.0.0",
    #     port=8143
    # )