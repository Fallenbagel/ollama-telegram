import aiohttp
import json
from dotenv import load_dotenv
import os
load_dotenv()
system_info = os.uname()
token = os.getenv("TOKEN")
allowed_ids = list(map(int, os.getenv('USER_IDS', '').split(',')))
admin_ids = list(map(int, os.getenv('ADMIN_IDS', '').split(',')))
# Will be implemented soon
#content = []

async def fetcher():
    async with aiohttp.ClientSession() as session:
        url = 'http://localhost:11434/api/tags'
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data['models']
            else:
                return []


async def streamer(prompt: str, modelname: str):
    #try:
        async with aiohttp.ClientSession() as session:
            print("Api triggered")
            url = 'http://localhost:11434/api/generate'
            #content.append(prompt)
            #print(f'Content updated: {content}')
            data = {
                "model": modelname,
                "prompt": prompt,
                "stream": True,
                #"context": content
            }
            print(f"DEBUG\n{modelname}\n{prompt}")
            # Stream from API
            async with session.post(url, json=data) as response:
                async for chunk in response.content:
                    if chunk:
                        decoded_chunk = chunk.decode()
                        if decoded_chunk.strip():
                            yield json.loads(decoded_chunk)
   # except:
   #     print("---------\n[Ollama-API ERROR]\nNON_DOCKER: Make sure your Ollama API server is running ('ollama serve' command)\nDOCKER: Check Ollama container and try again\n---------")