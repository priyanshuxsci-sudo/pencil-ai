import json
import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()
API_KEY = os.getenv("GEMINI_PLANNER_API")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemma-4-31b-it:generateContent?key={API_KEY}"


headers = {"Content-Type": "application/json"}


def ask_gemini(contents):
    for ch in "------------------------------\nPlanner Executed.":
    	print(ch,end="", flush=True)
    	time.sleep(0.015)
    	
    payload = {"contents":contents}

    for _ in range(2):
    	try:
    		response = requests.post(url, headers=headers, json=payload)
    		print(f"\n(PLANNER TOKEN COST: {response.json()["usageMetadata"]["totalTokenCount"]})")
    		return response.json()["candidates"][0]["content"]["parts"][-1]["text"]
    	except (KeyError, requests.exceptions.SSLError, requests.exceptions.ConnectionError):
    		try:
    			return f"Status Code: {response.status_code} Raw Response: {response.text}"
    		except NameError:
    			print("SERVER NOT RESPONDING ‼️. Retrying Soon..")
    			continue
    		print("SERVER NOT RESPONDING ‼️. Retrying Soon..")
    		continue
