import json
import request
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_PLANNER_API")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemma-4-31b-it:generateContent?key={API_KEY}"


headers = {"Content-Type": "application/json"}


def ask_gemini(contents):
    print("------------------------------\nPlanner Executed.")
    payload = {"contents":contents}

    response = requests.post(url, headers=headers, json=payload)
    
    print(f"[*PLANNER TOKEN COST: {response.json()["usageMetadata"]["totalTokenCount"]}]")

    try:
        return response.json()["candidates"][0]["content"]["parts"][-1]["text"]
    except Exception as e:
        return f"Status Code: {response.status_code} Raw Response: {response.text}"
