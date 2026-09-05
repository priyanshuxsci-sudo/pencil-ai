import requests
import json
import os
import time
from dotenv import load_dotenv
load_dotenv()

API_KEY2 = os.getenv("GEMINI_TALK_API")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemma-4-31b-it:generateContent?key={API_KEY2}"

headers = {"Content-Type": "application/json",
"x-goog-api-key": API_KEY2
}
#GOOGLE

#Required set for Curator
API_KEY = os.getenv("GROQ_API")

URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
#GROQ

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


# Load past turns ONCE when this module is imported (i.e. when main.py starts)
load_previous_history()


def talk_gemini(question):

    contents.append({"role": "user", "parts": [{"text": question}]})

    payload = {
        "contents": contents,
        "systemInstruction": {
            "parts": [
                {
                    "text": (
                        "Don't even Daire to answer in Big Paragraph Format. Be Pointwise. You are PENCIL.ai. Answer in a simple format, and in very "
                        "easy and understandable way. Also, be more energetic and "
                        "use lots of emojis. Answers should always be truthful and real. Don't Use Pointwise Format Unless Required. Be morr Decorative in OutPut"
                    )
                }
            ]
        },
    }

    response = requests.post(url, headers=headers, json=payload)

    try:
        answer1 =response.json()["candidates"][0]["content"]["parts"][-1]["text"]
        answer2= f"[*Chat Token Cost: {response.json()["usageMetadata"]["totalTokenCount"]}]\n  Prompt: {response.json()["usageMetadata"]["promptTokenCount"]}\n  OutPut: {response.json()["usageMetadata"]["candidatesTokenCount"]}\n"+ "-"*30 + "\n\n"
        
        answer = answer2 + answer1
    except (KeyError, IndexError):
        answer = f"Error or empty response: {result}"
        return answer

    contents.append({"role": "model", "parts": [{"text": answer}]})

    with open(CHAT_FILE, "a", encoding="utf-8") as f:
        f.write(f"User: {question}\n")
        f.write(f"Gemini: {answer1}\n\n")
        

    return answer


def curator(save):
    # 2. Define the payload
    payload = {
        "model": "openai/gpt-oss-120b",  # Replace with your desired model ID
        "messages": [
            {
                "role": "system",
                "content": "Take the Abstract provided, which is an Output of some tool, and present it in Good Formart. Like don't change the content of the OutPut. Use Lots Of Emojis, and give like a  real feel and energy. Without Changing the Content."
            },
            {
                "role": "user",
                "content": save
            }
        ],
        "temperature": 0.7,
        "max_tokens": 2000,
    }

    # 3. Make the API call
    response = requests.post(URL, headers=HEADERS, json=payload)
    

    if response.status_code == 200:
        tokens = f"[Token Used = {response.json()["usage"]["total_tokens"]}]\n------------------------------\n\n"
        text = response.json()["choices"][0]["message"]["content"]
        
        return tokens + text
    else:
        return f"ERROR {response.status_code}: {response.text}"


def wiki(place):
    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": place,
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
    }

    HEADERS = {
        "User-Agent": "Myprojectnamedpencil.ai/1.0 priyanshu.xsci@gmail.com"
    }

    response = requests.get(url=URL, params=PARAMS, headers=HEADERS)

    data = response.json()
    page = next(iter(data["query"]["pages"].values()))

    save = page["extract"]
    results = curator(save)

    return results
    
    
def talk_deep():
    print("✨DEEPTALK PENCIL.ai")
    print("Use Command .break to exit.")
    while True:
        ask = input("\n\nAsk Anything: ")
        
        if ask == ".break":
        	break

        contents.append({"role": "user", "parts": [{"text": ask}]})

        payload = {
            "contents": contents,
            "systemInstruction": {
                "parts": [
                    {
                        "text": (
                            "Don't even Daire to answer in Big Paragraph Format. You are PENCIL.ai. Answer in a simple format, and in very "
                            "easy and understandable way. Also, be more energetic and "
                            "use lots of emojis. Answers should always be truthful and real. Don't Use Pointwise Format Unless Required. Be morr Decorative in OutPut"
                        )
                    }
                ]
            },
        }

        response = requests.post(url, headers=headers, json=payload)

        try:
            answer1 = response.json()["candidates"][0]["content"]["parts"][-1]["text"]
            answer2 = "="*30+f"\n[*Chat Token Cost: {response.json()["usageMetadata"]["totalTokenCount"]}]\n    Prompt: {response.json()["usageMetadata"]["promptTokenCount"]}\n    OutPut: {response.json()["usageMetadata"]["candidatesTokenCount"]}\n"+ "="*30 + "\n\n"

            answer = answer2 + answer1
        except (KeyError, IndexError):
            answer = f"Error or empty response: {result}"
            return answer

        contents.append({"role": "model", "parts": [{"text": answer}]})

        with open(CHAT_FILE, "a", encoding="utf-8") as f:
            f.write(f"User: {ask}\n")
            f.write(f"Gemini: {answer1}\n\n")
            
            print()

            for ch in "✨ PENCIL.ai":
                print(ch, end="", flush=True)
                time.sleep(0.375)
            print()
            
            for _ in answer:
            	print(_, end="",flush=True)
            	time.sleep(0.02)
            	

    return answer