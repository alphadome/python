import pygal
from die import Die

#Creat a D6.
die_1 = Die()
die_2 = Die(10)

#make some rolls and store in a list
results = [ ]
for roll_num in range(100000):
	result = die_1.roll() + die_2.roll()
	results.append(result)


# analyze the results
frequencies = []

max_result = die_1.num_sides + die_2.num_sides
for value in range(2,max_result+1):
	frequency = results.count(value)
	frequencies.append(frequency)

#Visualize the results.
hist = pygal.Bar()

hist.title = "Results of rolling one D6 1000 times."
xlabel =[ ]
for label_num in range(1,max_result+1):
	xlabel.append(label_num)

hist.x_labels = xlabel

hist.x_title = "Result"
hist.y_title = "Frequency of Result"

hist.add('D6', frequencies)
hist.render_to_file('die_visual.svg')
