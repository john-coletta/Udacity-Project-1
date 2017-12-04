import csv
from datetime import datetime
from pprint import pprint
import matplotlib.pyplot as plt

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
#Create a dictionary for the cleaned files
cleaned_files = {'Washington': directory + '/data/Washington-2016-Summary.csv', 
'NYC': directory + '/data/NYC-2016-Summary.csv', 
'Chicago': directory + '/data/Chicago-2016-Summary.csv'}

for city in cleaned_files:
	print('{}: {}'.format(city,number_of_trips(cleaned_files[city])))
#Calculate the max number of trips  
max_trips = 0
for city in cleaned_files:
	new_max = number_of_trips(cleaned_files[city])[2]
	if new_max > max_trips:
		max_trips = new_max
		biggest_city = city

print('{} had the most trips in 2016 with {}.'.format(biggest_city, max_trips))
#Calculate the number of trips by subscribers
sub_trips = 0

for city in cleaned_files:
	print(city)
	city_subs = float(number_of_trips(cleaned_files[city])[0]) / number_of_trips(cleaned_files[city])[2]
	print(city_subs)
	if city_subs > sub_trips:
		sub_trips = city_subs
		print(sub_trips)
		city_with_highest_sub_ratio = city
		
pct_subs = 100 * sub_trips

print('{} had the highest proportion of trips made by subscribers with {}% of the total trips.'.format(city_with_highest_sub_ratio, round(pct_subs, 2)))
#Calculate the number of trips by non-subscribers
non_sub_trips = 0
for city in cleaned_files:
	city_non_subs = float(number_of_trips(cleaned_files[city])[1]) / number_of_trips(cleaned_files[city])[2]
	if city_non_subs > non_sub_trips:
		non_sub_trips = city_non_subs
		city_with_highest_non_sub = city
pct_non_subs = 100 * non_sub_trips

print('{} had the highest proportion of trips made by short-term customers with {}% of the total trips.'.format(city_with_highest_non_sub, round(pct_non_subs, 2)))

def avg_duration(filename, n=2):
	'''
	This function calculates the average duration of a trip in a certain city to n(default 2)
	decimal places.
	'''
	with open(filename, 'r') as f_in:
		reader = csv.DictReader(f_in)
        #sum up the total duration of trips
		total_duration = 0
		for row in reader:
			total_duration = total_duration + float(row['duration'])
        #divide by total number of trips to get average    
		average_duration = total_duration / number_of_trips(filename)[2]
        
		return round(average_duration, n)

def overage_trips(filename, n=2):
	'''This function calculates the proportion of rides over 30 minutes in a city to n(default 2)
	decimal places.
	'''
	with open(filename, 'r') as f_in:
		reader = csv.DictReader(f_in)
        #initialize counter for trips over 30 min
		over_30 = 0
		for row in reader:
			if float(row['duration']) > 30.0:
				over_30 += 1
                
		pct_over_30 = (float(over_30) / number_of_trips(filename)[2]) * 100.0
        
		return round(pct_over_30, n)

for city in cleaned_files:
	print('The average trip duration in {} was {} minutes. {}% of the trips were over 30 minutes, and thus subject to overage charges.'.format(city, avg_duration(cleaned_files[city]), overage_trips(cleaned_files[city])))
	
def user_ride_duration(filename, n=2):
	'''This function determines the average ride duration (to n(default 2) decimal places) for each subset of rider and returns
	the average duration for each of those groups.'''
	with open(filename, 'r') as f_in:
		reader = csv.DictReader(f_in)
		
		subs_duration = 0
		non_subs_duration = 0
		for row in reader:
			if row['user_type'] == 'Subscriber':
				subs_duration = subs_duration + float(row['duration'])
			else:
				non_subs_duration = non_subs_duration + float(row['duration'])
            
		subs_avg_duration = subs_duration / number_of_trips(filename)[0]
		non_subs_avg_duration = non_subs_duration / number_of_trips(filename)[1]
        
		if subs_avg_duration > non_subs_avg_duration:
			longer_rider = 'Subscribers'
		elif subs_avg_duration == non_subs_avg_duration:
			longer_rider = 'Neither'
		else:
			longer_rider = 'Customers'
        
		return(round(subs_avg_duration, n), round(non_subs_avg_duration, n), longer_rider)
#Will choose Chicago for all further questions, but calculating all of the cities here isn't hard  
for city in cleaned_files:
	print('In {} the subscribers had an average ride duration of {} minutes while the short-term customers had an average ride duration of {} minutes. This means that {} took a longer ride, on average.'.format(city, user_ride_duration(cleaned_files[city])[0], user_ride_duration(cleaned_files[city])[1], user_ride_duration(cleaned_files[city])[2]))
	
sub_durations = []
non_sub_durations = []
with open(cleaned_files['Chicago'], 'r') as f_in:
	Chicago_reader = csv.DictReader(f_in)
	
	for row in Chicago_reader:
		if row['user_type'] == 'Subscriber':
			sub_durations.append(float(row['duration']))
		else:
			non_sub_durations.append(float(row['duration']))
	
plt.hist(sub_durations, bins=75//5, range=(0,75))
plt.title('Distribution of Duration of Subscriber Trips (Chicago)')
plt.xlabel('Duration (min)')
plt.savefig('sub_histogram_chicago.png')
plt.show()

plt.clf()

plt.hist(non_sub_durations, bins=75//5, range=(0,75))
plt.title('Distribution of Duration of Non-Subscriber Trips Chicago)')
plt.xlabel('Duration (min)')
plt.savefig('non_sub_historgram_chicago.png')
plt.show()
#Now looking at trips in various cities by month
def trips_by_month(filename):
    '''This function will take one data set and month as int 1-12 and return a dictionary
    of the trips by month'''
    month_trips = {}
    
    with open(filename, 'r') as f_in:
        reader = csv.DictReader(f_in)
        
        for row in reader:
            if str(row['month']) not in month_trips:
                month_trips[str(row['month'])] = 1
            else:
                month_trips[str(row['month'])] += 1
        
    return month_trips

def month_graphs(filename, city, filename1=None, city1=None, filename2=None, city2=None):
    '''This function takes a filename (up to three) and city name (up to three again) and plots the month to month trip data
    on a bar cart.'''
    month_file = trips_by_month(filename)
    month_data = []
    numerals = []
    numerals_set = numerals
    month_labels = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')
    width = 0.3
    for n in range(1,13):
        month_data.append(month_file[str(n)])
        numerals.append(n)
        
    if filename1:
        month_file1 = trips_by_month(filename1)
        month_data1 = []
        for n in range(1,13):
            month_data1.append(month_file1[str(n)])
    
    if filename2:
        month_file2 = trips_by_month(filename2)
        month_data2 = []
        for n in range(1,13):
            month_data2.append(month_file2[str(n)])
            
    fig, ax = plt.subplots()
    
    bar1 = ax.bar(numerals, month_data, width, color='r')
    
    if filename1:
        for n in range(0,12):
            numerals[n] = numerals[n] + width
        bar2 = ax.bar(numerals, month_data1, width, color='b')
        
    if filename2:
        for n in range(0,12):
            numerals[n] = numerals[n] - (2 * width)
        bar3 = ax.bar(numerals, month_data2, width, color='y')
        
    ax.set_ylabel('Number of Trips')
    ax.set_title('Number of Bike-Share Trips per Month in Selected Cities')
    ax.set_xticks(numerals_set)
    ax.legend(bar1, city)
    if city1:
        ax.legend((bar1, bar2), (city, city1))
    if city2:
        ax.legend((bar1, bar2, bar3), (city, city1, city2))
    
    ax.set_xticklabels(month_labels)
    plt.savefig('month_data.png')
    plt.show()
    
month_graphs(cleaned_files['NYC'], 'NYC', cleaned_files['Chicago'], 'Chicago', cleaned_files['Washington'],'Washington')

def seasonal_data(month_data):
    '''Takes the output of trips_by_month and returns seasonal data
    '''
    winter = 0
    spring = 0
    summer = 0
    fall = 0
    for n in ['12','1','2']:
        winter = winter + month_data[n]
    for n in ['3','4','5']:
        spring = spring + month_data[n]
    for n in ['6','7','8']:
        summer = summer + month_data[n]
    for n in ['9','10','11']:
        fall = fall + month_data[n]
        
    
    return (winter, spring, summer, fall)

nycseasons = seasonal_data(trips_by_month(cleaned_files['NYC']))
washingtonseasons = seasonal_data(trips_by_month(cleaned_files['Washington']))
chicagoseasons = seasonal_data(trips_by_month(cleaned_files['Chicago']))

print('NYC has {} trips in the winter, {} trips in the spring, {} trips in the summer, and {} trips in the fall.'.format(nycseasons[0],nycseasons[1],nycseasons[2],nycseasons[3]))
print('Washington has {} trips in the winter, {} trips in the spring, {} trips in the summer, and {} trips in the fall.'.format(washingtonseasons[0],washingtonseasons[1],washingtonseasons[2],washingtonseasons[3]))
print('Chicago has {} trips in the winter, {} trips in the spring, {} trips in the summer, and {} trips in the fall.'.format(chicagoseasons[0],chicagoseasons[1],chicagoseasons[2],chicagoseasons[3]))

