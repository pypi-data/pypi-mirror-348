# from fastapi import WebSocket
# from litegen import LLM
# from liteutils import remove_references
#
# from .base import Feature
#
# import time
#
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# import json
# from openai import OpenAI
# import asyncio
# from liteauto import compress,web
#
#
# def streamer(res: str):
#     "simulating streaming by using streamer"
#     for i in range(0, len(res), 20):
#         time.sleep(0.001)
#         yield res[i:i + 20]
#
#
# async def handle_google_search(websocket: WebSocket, message: str):
#     """Handle Google search-like responses"""
#     try:
#         for chunk in streamer(message):
#             await websocket.send_text(json.dumps({
#                 "sender": "bot",
#                 "message": chunk,
#                 "type": "stream"
#             }))
#             await asyncio.sleep(0.001)
#
#         await websocket.send_text(json.dumps({
#             "sender": "bot",
#             "type": "end_stream"
#         }))
#
#     except Exception as e:
#         await websocket.send_text(json.dumps({
#             "sender": "bot",
#             "message": f"Error: {str(e)}",
#             "type": "error"
#         }))
#
# class FastGoogleSearch(Feature):
#     """Google search feature implementation"""
#
#     async def handle(self, websocket: WebSocket, message: str, system_prompt: str,
#                      chat_history=None,**kwargs):
#         from liteauto import google,wlanswer
#         from liteauto.parselite import aparse
#
#         max_urls = kwargs.get("is_websearch_k", 3)
#         urls = google(message, max_urls=max_urls)
#
#         web_results = await aparse(urls)
#         web_results = [w for w in web_results if w.content]
#
#         ctx = ""
#
#         res = ""
#         for w in web_results:
#             try:
#                 if 'arxiv' in w.url:
#                     content = remove_references(w.content)
#                 else:
#                     content = w.content
#                 ans = wlanswer(content,message,k=2)
#                 ctx += ans+ "\n"
#                 res += f"Source: [{w.url}]\n\n{ans}\n"
#                 res += f"-"*50 + "\n"
#             except:
#                 pass
#         llm = LLM(api_key=kwargs['api_key'])
#         llm_answer = llm(system_prompt="You are Answer summarize, answer the user question with context more detailed way",
#                          prompt=f"context: {ctx}\n\n question: {message}")
#
#         await handle_google_search(websocket=websocket,
#                                    message=llm_answer)
#
#     # async def handle(self, websocket: WebSocket, message: str, system_prompt: str,
#     #                  chat_history=None,**kwargs):
#     #     from liteauto import google,wlanswer
#     #     from liteauto.parselite import aparse
#     #
#     #     max_urls = kwargs.get("is_websearch_k", 3)
#     #     urls = google(message, max_urls=max_urls)
#     #
#     #     web_results = await aparse(urls)
#     #     web_results = [w for w in web_results if w.content]
#     #
#     #     res = ""
#     #     for w in web_results:
#     #         try:
#     #             if 'arxiv' in w.url:
#     #                 content = remove_references(w.content)
#     #             else:
#     #                 content = w.content
#     #             ans = wlanswer(content,message,k=2)
#     #             res += f"Source: [{w.url}]\n\n{ans}\n"
#     #             res += f"-"*50 + "\n"
#     #         except:
#     #             pass
#     #
#     #     await handle_google_search(websocket=websocket,
#     #                                message=res)
#
#


import os
from concurrent.futures import ThreadPoolExecutor

from litegen import LLM
from liteutils import remove_references

from .base import Feature


from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
import asyncio

async def llm_streamer(message,api_key,model,is_websearch_k):
    from liteauto.searchlite import google
    from liteauto.visionlite import wlanswer
    from liteauto.parselite import aparse

    max_urls = is_websearch_k if is_websearch_k else 10
    urls = google(message, max_urls=max_urls)

    web_results = await aparse(urls)
    web_results = [w for w in web_results if w.content]

    ctx = ""

    res = ""
    for w in web_results:
        try:
            if 'arxiv' in w.url:
                content = remove_references(w.content)
            else:
                content = str(w.content)
            ans = wlanswer(content,message,k=is_websearch_k) if is_websearch_k else content
            ctx += ans+ "\n"
            res += f"Source: [{w.url}]\n\n{ans}\n"
            res += f"-"*50 + "\n"
        except:
            pass
    llm = LLM(api_key=api_key)
    for x in llm.completion(system_prompt="You are Answer summarize, answer the user question with context more detailed way,"
                                          "if context is empty/None, let user knwo without google result., if paper related they provide "
                                          "summary of it.",
                     prompt=f" user query: {message} \n\n context: {ctx}\n\n",
                            model=model,response_format=None,stream=True):
        if x:
            yield x.choices[0].delta


async def _handle_web_search(websocket: WebSocket, message: str,api_key:str,model:str,is_websearch_k):
    """Handle Google search-like responses"""

    try:
        async for chunk in llm_streamer(message,api_key,model,is_websearch_k):
            await websocket.send_text(json.dumps({
                "sender": "bot",
                "message": chunk.content,
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


class FastGoogleSearch(Feature):
    """Google search feature implementation"""


    async def handle(self, websocket: WebSocket, message: str, system_prompt: str,
                     chat_history=None, **kwargs):

        await _handle_web_search(websocket=websocket,
                                 message=message,
                                 api_key=kwargs.get('api_key'),
                                 model=kwargs.get("model"),
                                 is_websearch_k=kwargs.get("is_websearch_k"))
