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
		s = float(millis) / 1000
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
	
def type_of_user(datum, city):
	'''Takes a dictionary containing info about a single trip as input(datum)
	and its origin city and returns the type of system user that made the trip
	'''
	if city == 'Chicago':
		user_type = datum['usertype']
	if city == 'NYC':
		user_type = datum['usertype']
	if city == 'Washington':
		user_type1 = datum['Member Type']
		if user_type1 == 'Registered':
			user_type = 'Subscriber'
		if user_type1 == 'Casual':
			user_type = 'Customer'
			
	return user_type
	
def condense_data(in_file, out_file, city):
	'''
	Takes the full data from input file and condenses
	it into specified output file, city determines how data is parsed.
	Uses helper fuctions from above.
	'''
	with open(out_file, 'wb') as f_out, open(in_file) as f_in:
		out_colnames = ['duration', 'month', 'hour', 'day_of_week', 'user_type']
		trip_writer = csv.DictWriter(f_out, fieldnames = out_colnames)
		trip_writer.writeheader()
		
		trip_reader = csv.DictReader(f_in)
		
		for row in trip_reader:
			new_point = {out_colnames[0]:duration_in_mins(row, city),
                         out_colnames[1]:time_of_trip(row, city)[0],
                         out_colnames[2]:time_of_trip(row, city)[1],
                         out_colnames[3]:time_of_trip(row, city)[2],
                         out_colnames[4]:type_of_user(row, city)}
            
			trip_writer.writerow(new_point)

city_info = {'Washington': {'in_file': data_files[2],
                            'out_file': directory + '/data/Washington-2016-Summary.csv'},
             'Chicago': {'in_file': data_files[1],
                         'out_file': directory + '/data/Chicago-2016-Summary.csv'},
             'NYC': {'in_file': data_files[0],
                     'out_file': directory + '/data/NYC-2016-Summary.csv'}}

for city, filenames in city_info.items():
    condense_data(filenames['in_file'], filenames['out_file'], city)

''' Now write functions to perform statistical analysis on the data sets
'''

def number_of_trips(filename):
    """
    This function reads in a file with trip data and reports the number of
    trips made by subscribers, customers, and total overall.
    """
	with open(filename, 'r') as f_in:
        # set up csv reader object
		reader = csv.DictReader(f_in)
        
        # initialize count variables
		n_subscribers = 0
		n_customers = 0
        
        # tally up ride types
		for row in reader:
			if row['user_type'] == 'Subscriber':
				n_subscribers += 1
			else:
				n_customers += 1
        
        # compute total number of rides
		n_total = n_subscribers + n_customers
        
        # return tallies as a tuple
		return(n_subscribers, n_customers, n_total)
	