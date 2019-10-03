def get_formatted_name(first_name, last_name):
	"""Return a full name neatly formatted"""
	full_name = first_name + " " + last_name
	return full_name.title()

#this is an infinite loop
while True:
	print("\nPlease tell me your name: \nenter q to quit.  ")
	f_name = input("First name:  ")
	if f_name == "q":
			break
	l_name = input("Last name:  ")
	if l_name =="q":
			break
	formatted_name = get_formatted_name(f_name, l_name)
	print("\nHello "+ formatted_name + "!")
