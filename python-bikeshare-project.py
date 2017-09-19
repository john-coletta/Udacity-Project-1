import csv
from datetime import datetime
from pprint import pprint

directory = 'C:/John/Programming/Code/Udacity/Part 2'

data_files = [directory + '/data/NYC-CitiBike-2016.csv',
			  directory + '/data/Chicago-Divvy-2016.csv',
			  directory + '/data/Washington-CapitalBikeshare-2016.csv']
 
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
	
def duration_in_mins(datum, city):
	''' Takes a dictionary with info about a single trip as input(datum) 
	and its origin city and returns the duration of the trip
	in minutes.
	'''
	
	if city == 'Washington':
		millis = datum['Duration (ms)']
		s = float(ms) / 1000
		duration = s / 60
	if city == 'Chicago' or city == 'NYC':
		s = datum['tripduration']
		duration = float(s) / 60
		
	return duration
	
def time_of_trip(datum, city):
	''' Takes a dictionary with info about a single trip as input(datum)
	and its origin city and returns the month, hour, and day of the week
	the trip was made.
	'''
	if city == 'Washington':
        date = datum['Start date']
        #Convert to datetime object via strptime
        d = datetime.strptime(date, '%m/%d/%Y %H:%M')
        month = d.month
        hour = d.hour
        day_of_week = d.strftime('%A')
    if city == 'NYC':
        date = datum['starttime']
        d = datetime.strptime(date, '%m/%d/%Y %H:%M:%S')
        month = d.month
        hour = d.hour
        day_of_week = d.strftime('%A')
    if city == 'Chicago':
        date = datum['starttime']
        d = datetime.strptime(date, '%m/%d/%Y %H:%S')
        month = d.month
        hour = d.hour
        day_of_week = d.strftime('%A')
		
	return (month, hour, day_of_week)
	