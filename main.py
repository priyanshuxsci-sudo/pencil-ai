import time

print(" "*10+"="*40+"\n"+" "*17+"PENCIL.ai USER INTERFACE."+"\n"+" "*10+"="*40)

clear = input('Commond Line :-\n".clear" To Clear Chat History. Else Enter😊\n')

if clear == ".clear":
	with open("chat_history.txt", "r+") as f:
			f.seek(0)
			f.truncate()
			print("Cleared")

print()
from planners import planner
from registry import TOOL
from Tools import talk_deep
import sys
from resoning import resoning

print("-"*20+"\n"+" "*5+" ‼️ NOTE"+"\n"+"-"*20)
for l in "Plugin's Available :\n •@Deep Talk/Conversation\n •@Resoning\n *NOTE : Plugin's, will Specifically Executed, if Typed in Ordered Format.\nFor Example:\n@Research and then Press Enter.\n\n• NEW CONVERSATIONS CAN BE STARTED ONLY IN DEEP TALK CONVERSATIONS. (IT WILL NOT DELETE THE PREVIOUS HISTORY) 👾\n":
	print(l, end="", flush=True)
	time.sleep(0.0075)

while True:
	print()
	for i in "Ask Anything":
		print(i, end="", flush=True)
		time.sleep(0.017)
	question = input(": ").strip()
	print()
	
	if question == ".exit":
		break
	elif question == ".clear":
		with open("chat_history.txt", "r+") as f:
			f.seek(0)
			f.truncate(0)
			print("Cleared")
			continue
	elif question in ["@Deep Talk", "@Conversation", "@dt"]:
		talk_deep()
		print()
		sys.exit("✨ KEEP LEARNING AND KEEP EXPLORING\n...MEET YOU AGAIN!\n🇮🇳 JAI HIND")
	elif question in ["@Resoning", "@resoning", "@r"]:
		r_ask = input("Ask Resoning.ai -> ")
		resoning(r_ask)
		sys.exit("✨ KEEP LEARNING AND KEEP EXPLORING\n...MEET YOU AGAIN!\n🇮🇳 JAI HIND")
		
	decision = planner(question)
	
	tool_name = decision["tool"]
	tool_input = decision["input"]
	
	ans = TOOL[tool_name](tool_input)
	
	for ch in ans + "\n":
		print(ch,end = "", flush=True)
		time.sleep(0.02)
