colours = ['blue', 'red', 'green', 'yellow']
print(colours[0].title())
print(colours[-1].title())
print(colours)
colours.append('black')
print(colours)
colours.insert(2, 'purple')
print(colours)
del colours[0]
print(colours)
colours.sort()
print(colours)
colours.sort(reverse=True)
print(colours)

print("here is the original list")
print(colours)
print("here is the sorted list")
print(sorted(colours))
len(colours)
print(len(colours))
for colour in colours:
	print(colour.title() + " what a shit colour")
print("Thank you colours for showing up!")
