available_toppings = ['mushrooms', 'olives', 'green peppers','pepperoni', 'pineapple', 'extra cheese']
requested_toppings = ['mushrooms', 'french fries', 'extra cheese','penguins']

if requested_toppings:
	for requested_topping in requested_toppings:
		if requested_topping in available_toppings:
			print("Adding " + requested_topping + ".")
		else:
			print("Sorry, we don't have " + requested_topping + ".")
	print("\nFinished making your pizza!")
else:
	print("Are you sure you want a plain pizza?")
