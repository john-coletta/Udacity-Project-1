import csv
from datetime import datetime
from pprint import pprint

data_files = ['./data/NYC-CitiBike-2016.csv',
			  './data/Chicago-Divvy-2016.csv',
			  './data/Washington-CapitalBikeshare-2016.csv']
 
def print_first_point(filename):
'''
Prints and returns first data point from
a csv file that inlcudes a header row
'''
	city = filename.split('-')[0].split('/')[-1]
	print('\nCity: {}'.format(city))
	
	with open(filename) as f_in:
	#set up the ordered reader with header as fieldnames
		trip_reader = csv.DictReader(f_in)
		
		#define the first trip
		first_trip = next(trip_reader)
		pprint(first_trip)
		
	return(city, first_trip)

example_trips = {}
for data in data_files:
	city, first_trip = print_first_point(data)
	example_trips[city] = first_trip
	
print(example_trips)