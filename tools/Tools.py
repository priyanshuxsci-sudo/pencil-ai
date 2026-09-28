import requests
import json
import os
import time
from dotenv import load_dotenv
load_dotenv()
from back_up import chat_back

API_KEY2 = os.getenv("GEMINI_TALK_API")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash-lite:generateContent?key={API_KEY2}"

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

def talk_gemini(question):
    contents.append({
        "role": "user",
        "parts": [{"text": question}]
    })

    payload = {
        "contents": contents,
        "systemInstruction": {
            "parts": [
                {
                    "text": (
                        "Use BIG Headlines, and Emoji's"
                    )
                }
            ]
        },
    }

    for _ in range(3):
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload
            )

            answer1 = response.json()["candidates"][0]["content"]["parts"][-1]["text"]

            usage = response.json()["usageMetadata"]

            answer2 = (
                "." * 30
                + f"\n(Chat Token Cost: {usage['totalTokenCount']})"
                + f"\n.Prompt: {usage['promptTokenCount']}"
                + f"\n.OutPut: {usage['candidatesTokenCount']}\n"
                + "." * 30
                + "\n\n"
            )

            answer = answer2 + answer1

            contents.append({
                "role": "model",
                "parts": [{"text": answer}]
            })

            with open(CHAT_FILE, "a", encoding="utf-8") as f:
                f.write(f"User: {question}\n")
                f.write(f"Gemini: {answer1}\n\n")

            print()

            return answer + "\n\nNOTE: If You Want To Dive Deeper, You can Simply Type Explain me 'SomeThing' Deeply."

        except (
            KeyError,
            IndexError,
            requests.exceptions.SSLError
        ):
            for i in "\n❌ API Call TimeOut. Retrying.":
                print(i, end="", flush=True)
                time.sleep(0.02)

            for j in "...\n" + "." * 30:
                print(j, end="", flush=True)
                time.sleep(0.1)
            continue
    print("‼️API UNDER MAINTENANCE!\nRedirecting to NVIDIA INTERFACE")
    answer_n = chat_back(question)
    return answer_n


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
        for i in "\n\n Ask Anything":
        	print(i , end="", flush=True)
        	time.sleep(0.017)
        ask = input(": ")
        print()
        
        if ask == ".break":
        	return "THANKS"

        contents.append({"role": "user", "parts": [{"text": ask}]})

        payload = {
            "contents": contents,
            "systemInstruction": {
                "parts": [
                    {
                        "text": (
                            "You are PENCIL.ai. Answer in a simple format, and in very "
                        "easy and understandable way. Also, be more energetic and "
                        "yah very deep in your words and be Philosophical and merge "
                        "this things in answer so well, that User should Not Notic, "
                        "How deep and Philosophical you've gone in that Topic. "
                        "Use a bit of emojis for Engagement. Answers should always "
                        "be truthful and real. Don't be Much Decorative, Answer in "
                        "Beautifully Great Format."
                        )
                    }
                ]
            },
        }
        
        for _ in range(3):
            try:
            	response = requests.post(url, headers=headers, json=payload)
            	answer1 = response.json()["candidates"][0]["content"]["parts"][-1]["text"]
            	answer2 = "."*30+f"\n(Chat Token Cost: {response.json()["usageMetadata"]["totalTokenCount"]})\n    Prompt: {response.json()["usageMetadata"]["promptTokenCount"]}\n    OutPut: {response.json()["usageMetadata"]["candidatesTokenCount"]}\n"+ "."*30 + "\n\n"
            	answer = answer2 + answer1
            	contents.append({"role": "model", "parts": [{"text": answer}]})
            	with open(CHAT_FILE, "a", encoding="utf-8") as f:
            		f.write(f"User: {ask}\n")
            		f.write(f"Gemini: {answer1}\n\n")
            		print()
            		for ch in "✨ PENCIL.ai\n\n":
            		  print(ch, end="", flush=True)
            		  time.sleep(0.075)
            		for _ in answer + "\n":
            			print(_, end="",flush=True)
            			time.sleep(0.02)
            		break
            	
            except (KeyError, IndexError, requests.exceptions.SSLError):
            		try:
            			answer = f"Error or empty response: {result}"
            		except NameError:
            			for i in "\n❌ API Call TimeOut. Retrying.":
            				print(i, end="", flush=True)
            				time.sleep(0.02)
            			for j in "...\n"+ "-"*30:
            				print(j, end="", flush=True)
            				time.sleep(0.1)
            		else:
            				for i in "\n❌ API Call TimeOut. Retrying.":
            					print(i, end="", flush=True)
            					time.sleep(0.02)
            				for j in "...\n"+"-"*30:
            					print(j, end="", flush=True)
            					time.sleep(0.1)
            		continue
            print("‼️API UNDER MAINTENANCE!\n Redirecting to NVIDIA INTERFACE")
            answer_n = chat_back(ask)
            pass
    return answer_n
