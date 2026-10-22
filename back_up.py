import requests
import os
from dotenv import load_dotenv
import time
load_dotenv()

invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
stream = True
API_KEY = os.getenv("NVIDIA_API")


headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
}
import json
CHAT_FILE = "chat_history.txt"
contents = []


def load_previous_history():
    """
    Rebuilds real {role, parts} turns from disk so the model actually
    remembers past sessions, instead of starting from contents = [].
    """
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

def chat_back(question):
    contents.append(question)

    payload = {
        "messages": [
            {
                "role": "user",
                "content": contents
            }
        ],
        "model": "deepseek-ai/deepseek-v4.1-flash",
        "max_tokens": 1024,
        "stream": True,
        "temperature": 0.7,
    }

    response = requests.post(
        invoke_url,
        headers=headers,
        json=payload,
        stream=True
    )

    answer1 = ""

    if stream:
        for line in response.iter_lines():
            if line:
                line_str = line.decode("utf-8")

                if line_str.startswith("data: "):
                    data_str = line_str[6:]

                    if data_str.strip() == "[DONE]":
                        break

                    try:
                        data = json.loads(data_str)
                        delta = data["choices"][0]["delta"]

                        if "content" in delta and delta["content"]:
                            answer1 += delta["content"]

                            print(
                                delta["content"],
                                end="",
                                flush=True
                            )

                            time.sleep(0.01)

                    except json.JSONDecodeError:
                        pass

    with open(CHAT_FILE, "a", encoding="utf-8") as f:
        f.write(f"User: {question}\n")
        f.write(f"Gemini: {answer1}\n\n")

    print()
    for i in answer1:
    	print(i, end="", flush=True)
    	time.sleep(0.01)

    return answer1