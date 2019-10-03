def make_pizza(size,*toppings):
	"""	print list of toppings that have been requested """
	print("\nMake "+str(size)+" inch pizza with the following ingredients:")
	for topping in toppings:
		print("-  " + topping)



