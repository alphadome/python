favourite_languages={
	'jen':'python',
	'sarah':'c',
	'edward':'ruby',
	'phil':'python',
	}
	
friends = ['phil', 'sarah']
for name in favourite_languages.keys():
	

	if name in friends:
		print("Hi " +name.title() +
		", I see your favourite language is "+
		favourite_languages[name].title() +"!")
	
	else:
		print(name.title())
