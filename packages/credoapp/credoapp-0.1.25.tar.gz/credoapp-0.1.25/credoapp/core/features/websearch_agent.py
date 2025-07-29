from litegen import LLM

from .base import Feature


from fastapi import  WebSocket
import json
import asyncio


def streamer(res: str):
    "simulating streaming by using streamer"
    for i in range(0, len(res), 20):
        yield res[i:i + 20]

from litegen import LLMSearch

async def _handle_web_search(websocket: WebSocket, message: str,api_key:str,model:str):
    """Handle Google search-like responses"""

    llm_search = LLMSearch(LLM(api_key),enable_think_tag=True,
                           model_name=model,
                           search_provider=None,
                           search_parallel=False)

    try:
        async for chunk in llm_search(message):
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


class WebSearchAgent(Feature):
    """Google search feature implementation"""


    async def handle(self, websocket: WebSocket, message: str, system_prompt: str,
                     chat_history=None, **kwargs):

        print(f'{kwargs=}')

        await _handle_web_search(websocket=websocket,
                                 message=message,
                                 api_key=kwargs.get('api_key'),
                                 model=kwargs.get("model"))
