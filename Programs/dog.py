class Dog():
	"""A simple attempt to model a dog."""
	
	def __init__(self, name, age):
		""" initialize name and age attributes."""
		self.name = name
		self.age = age
	
	def sit(self):
		""" simulate a dog sitting in response to a command."""
		print(self.name.title() + " is now sitting.")
		
	def roll_over(self):
		"""simulate rolling over in response to a command."""
		print(self.name.title() + " rolled over!")
		

my_dog = Dog('willie',6)
your_dog = Dog('lucy',3)

print("my dog's name is " + my_dog.name.title()+ ".")
print("my dog is " + str(my_dog.age) + " years old.")

print("your dog's name is " + my_dog.name.title()+ ".")
print("your dog is " + str(my_dog.age) + " years old.")

my_dog.sit()
your_dog.sit()
my_dog.roll_over()


