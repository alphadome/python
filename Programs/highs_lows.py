import csv
from datetime import datetime

from matplotlib import pyplot as plt

#get dates and high temperatures from file
filename = 'death_valley_2014.csv'

with open(filename) as f:
	reader = csv.reader(f)
	header_row = next(reader)
	
	dates, highs, lows = [], [], []
	for row in reader:
		try:
			current_date = datetime.strptime(row[0],"%Y-%m-%d")
			high = int(row[1])
			low = int(row[3])
		except ValueError:
			print(current_date, 'missing data')
		else:			
			dates.append(current_date)
			highs.append(high)
			lows.append(low)
		
#Plot data.
fig = plt.figure(dpi=80, figsize=(10,6))
plt.plot(dates, highs, c='red', alpha=0.5)
plt.plot(dates, lows, c='blue', alpha=0.5)
plt.fill_between(dates, highs, lows, facecolor='blue', alpha=0.1)

#Format plot.
plt.title("Daily high and low temperatures - 2014", fontsize=10)
plt.xlabel(' ', fontsize=8)
fig.autofmt_xdate()
plt.ylabel("Temperature (f)", fontsize=8)
plt.tick_params(axis='both', which='major', labelsize=8)

plt.show()
