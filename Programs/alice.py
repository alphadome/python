

def count_words(filename):
	"""count approximate amount of words in a file"""
	try:
		with open(filename) as f_obj:
			contents = f_obj.read()

	except FileNotFoundError:
		pass

	else:
		# Count the appropriate number of words in the file.
		words = contents.split()
		num_words = len(words)
		print("The file " + filename + " Has about " + str(num_words) + " words.")
	

def search_word(filename):
	"""count appearances of word in the file"""
	
	looper = True
		
	while looper:
	
		phrase = input("\nEnter the phrase you would like to search or 'q' to quit:  ")
	
		if phrase == 'q':
			looper = False
		
		else:
			try:
				with open(filename) as f_obj:
					contents = f_obj.read()
					print(contents.lower().count(phrase))
			
			except FileNotFoundError:
				pass

		

search_word('alice.txt')


filenames = ['alice.txt', 'siddhartha.txt', 'moby_dick.txt', 'little_women.txt']
for filename in filenames:
	count_words(filename)
	

