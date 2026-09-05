clear = input('Commond Line :-\n".clear" To Clear Chat History. Else Enter😊\n')

if clear == ".clear":
	with open("chat_history.txt", "r+") as f:
			f.seek(0)
			f.truncate()
			print("Cleared")


from planners import planner
from registry import TOOL
from Tools import talk_deep
import time
import sys

print("Plugin's Available :\n  @Deep Talk/Conversation")
print("*NOTE : Plugin's, will Specifically Executed, if Typed in Ordered Format.\nFor Example:\n@Research and then Press Enter.")

while True:
	print()
	
	question = input("\nAsk Anything: ").strip()
	print()
	
	if question == ".exit":
		break
	elif question == ".clear":
		with open("chat_history.txt", "r+") as f:
			f.seek(0)
			f.truncate(0)
			print("Cleared")
			continue
	elif question in ["@Deep Talk", "@Conversation"]:
		talk_deep()
		print()
		sys.exit("✨ KEEP LEARNING AND KEEP EXPLORING\n...MEET YOU AGAIN!\n🇮🇳 JAI HIND")
		
	decision = planner(question)
	
	tool_name = decision["tool"]
	tool_input = decision["input"]
	
	ans = TOOL[tool_name](tool_input)
	
	for ch in ans:
		print(ch,end = "", flush=True)
		time.sleep(0.02)