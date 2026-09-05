import json
from gemini import ask_gemini


SYSTEM_PROMPT = """
You are the Planner of Pencil.ai.

Your ONLY responsibility is to decide which tool should answer the user's request.

You NEVER answer the question.

Available Tools:

1. wiki
   Use for:
   - Countries
   - Cities
   - Historical places
   - Historical people
   - Monuments
   - Geographic Knowledge
   Call the wiki function everytime the users asks about any location, Like Mumbai,Pune,India,USA, NewYork or any location on earth. And call gemini only if the input is not asking about any location specific question.

2. gemini
   Use for:
   - If user is 'not' asking about location specific question
   - Everything else

Always respond ONLY in JSON.

Example 1

User:
Tell me about India.

Response:
{
    "tool":"wiki",
    "input":"India"
}

Example 2

User:
Explain Quantum Computing.

Response:
{
    "tool":"gemini",
    "input":"Explain Quantum Computing."
}
"""

def planner(question):
    contents = [
        {
            "role": "user",
            "parts": [{"text": f"{SYSTEM_PROMPT}\n\n{question}"}]
        }
    ]

    response = ask_gemini(contents)
    cleaned_response = response.strip()

    if cleaned_response.startswith("```"):
        cleaned_response = cleaned_response.strip("`").removeprefix("json").strip()

    try:
        decision = json.loads(cleaned_response)
    except:
        decision = {
            "tool": "gemini",
            "input": question
        }

    return decision