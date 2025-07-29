import json
import asyncio

from litegen import LLM
from fastapi import WebSocket

from .base import Feature



async def _handle_web_search(websocket: WebSocket, message: str,api_key:str,model:str):
    """Handle Google search-like responses"""
    try:
        async for chunk in LLM(message,
                                     model=model,
                                     api_key=api_key):
            await websocket.send_text(json.dumps({
                "sender": "bot",
                "message": chunk.content+"\n",
                "type": "stream"
            }))
            await asyncio.sleep(0.001)

        await websocket.send_text(json.dumps({
            "sender": "bot",
            "type": "end_stream"
        }))

    except Exception as e:
        await websocket.send_text(json.dumps({
            "sender": "bot",
            "message": f"Error: {str(e)}",
            "type": "error"
        }))


class SearchAgent(Feature):
    """Google search feature implementation"""


    async def handle(self, websocket: WebSocket, message: str, system_prompt: str,
                     chat_history=None, **kwargs):

        print(f'{kwargs=}')

        await _handle_web_search(websocket=websocket,
                                 message=message,
                                 api_key=kwargs.get('api_key'),
                                 model=kwargs.get("model"))
