def describe_pet(pet_name, animal_type = 'dog'):
	"""display information about pet"""
	print("\nI have a " + animal_type + ".")
	print("My "+ animal_type + " is called " + pet_name.title() + ".")

describe_pet(pet_name = "harry", animal_type = "parrot")
describe_pet("willie")
describe_pet("harry", "parrot")
