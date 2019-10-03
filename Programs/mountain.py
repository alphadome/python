responses = {}

#set a flag to indicate polling is active
polling_active = True

while polling_active:
	#prompt for persons name and response
	name = input("\nWhat is your name?  ")
	response = input("\nWhich mountain would you like to climb?  ")
	
	#store responses in dictionary
	responses[name] = response
	
	#find out who else will take the poll
	repeat = input("\n Anyone else to respond (y/n)? ")
	
	if repeat == 'n':
		polling_active = False


#polling inactive, show the results
print("\n ---Poll results---")

for name, response in responses.items():
	print(name.title() + " would like to climb " + response.title() + "suski.")
