import json
import time
import os
import requests
from dotenv import load_dotenv
load_dotenv

API_KEY2 = os.getenv("GEMINI_TALK_API")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemma-4-31b-it:generateContent?key={API_KEY2}"

headers = {"Content-Type": "application/json",
"x-goog-api-key": API_KEY2
}


CHAT_FILE = "chat_history.txt"
contents = []


def load_previous_history():
    if not os.path.exists(CHAT_FILE):
        return

    with open(CHAT_FILE, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        return

    blocks = text.split("\n\n")
    for block in blocks:
        block = block.strip()
        if block.startswith("User: ") and "\nGemini: " in block:
            user_part, model_part = block.split("\nGemini: ", 1)
            user_text = user_part[len("User: "):]
            contents.append({"role": "user", "parts": [{"text": user_text}]})
            contents.append({"role": "model", "parts": [{"text": model_part}]})


load_previous_history()

def follow_up(data):

    while True:
        print("Ask Anything Regarding This.")
        ask = input("Ask Follow Up: ")

        if ask == ".break":
            break

        contents.append({"role": "user", "parts": [{"text": ask}]})

        payload = {
            "contents": contents,
            "systemInstruction": {
                "parts": [
                    {
                        "text": (
                            f"This is the File You have been Provided {data} User will ask Questions On the Basis of this. Use Big Headlines, and Be Friendly."
                        )
                    }
                ]
            },
        }
        while True:
            try:
            	response = requests.post(url, headers=headers, json=payload)
            	answer = response.json()["candidates"][0]["content"]["parts"][-1]["text"]
            	for ch in answer:
            	   print(ch, end="", flush=True)
            	   time.sleep(0.0175)
            	contents.append({"role": "model", "parts": [{"text": answer}]})
            	with open("resoning_history.txt", "w") as f:
            	  	f.write(f"User: {ask}\n")
            	  	f.write(f"Gemini: {answer}\n\n")
            	break
            except (KeyError, IndexError):
            	try:
            		answer = f"Error or empty response: {result}"
            	except NameError:
            		print("IT's Taking Quite Longer. Stay there. 😏")
            		continue
            	print("IT's Taking Quite Longer. Stay there. 😏")
            	continue

    return
