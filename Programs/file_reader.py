filename = 'pi_million_digits.txt'

with open(filename) as file_object:
	lines = file_object.readlines()

pi_string = ''
for line in lines:
	pi_string += line.rstrip()

active = True

while active:
	birthday = input("\nEnter 'q' to quit. \nEnter your birthday in the for ddmmyy:  ")
	if birthday == 'q':
		active = False
	elif birthday in pi_string:
		print ("Your birthday appears in the first million digits of pi!")
		birthday_occurences = pi_string.count(birthday)
		a,b = pi_string.split(birthday, 1)
		actual_place = len(a)-1
		
		print ("It's first occurence is after " + str(actual_place) + " digits and it occurs " +str(birthday_occurences) + " times.")

	else:
		print("Your birthday doesn't appear in the first million. :(")
