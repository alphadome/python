prompt = "\nTell me something interesting and i will make it awesome:   "
prompt+= "\nenter quit to quit"
prompt+="\n "

active = True
while active:
	message = input(prompt)
	
	if message == "quit":
		active = False
		
	else:
		print(message)
