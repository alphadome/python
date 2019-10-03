prompt = "\nTell me something interesting and i will make it awesome:   "
prompt+= "\nenter quit to quit"
prompt+="\n "

message = ""
while message != 'quit':
	message = input(prompt)
	
	if message != 'quit':
		print(message + "suski")
