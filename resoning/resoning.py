import requests
import json
import time
from follow_up_resoning import follow_up
import os
from dotenv import load_dotenv
load_dotenv()


API_KEY = os.getenv("GROQ_API")
URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def resoning(q):
    print()
    for ch in "(The Data of this Resoning Conversation will Not be Stored in History ❌\n\n)":
    	print(ch, end="", flush=True)
    	time.sleep(0.01)
    	
    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": [
            {
                "role": "system",
                "content": "Be Pointwise. You are PENCIL.ai. Answer in a simple format, and in very "
                        "easy and understandable way. Also, be more energetic and "
                        "use lots of emojis. Answers should always be truthful and real. Don't Use Pointwise Format Unless Required. Be morr Decorative in OutPut. Use Deep Resoning"
            },
            {
                "role": "user",
                "content": q
            }
        ],
        "reasoning_effort": "high",
        "max_tokens": 4096,
        "temperature": 0.6
    }

    response = requests.post(URL, headers=HEADERS, json=payload)
    

    if response.status_code == 200:
        data = response.json()["choices"][0]["message"]["content"]
        for ch in data:
        	print(ch, end="", flush=True)
        	time.sleep(0.0050)
        follow_up(data)
        return "THIS WAS PENCIL.ai 😊"
    else:
        return f"ERROR {response.status_code}: {response.text}"
        
