import os
import pandas as pd



def check_valid_time(data, root, filename):
	# iterate over start and end times
	for index, row in data.iterrows():
		try:
			row['StartTime'] = pd.to_datetime(unicode(row['StartTime']))
		except ValueError as ve:
			print 'ERROR:', ve, 'in', root, filename
			print row

		try:
			row['EndTime'] = pd.to_datetime(unicode(row['EndTime']))
		except ValueError as ve:
			print 'ERROR:', ve, 'in', root, filename
			print row


def check_time_interval(data, root, filename):
	# iterate over start and end times
	for index, row in data.iterrows():
		try:
			row['StartTime'] = pd.to_datetime(unicode(row['StartTime']))
		except ValueError:
			continue
		try:
			row['EndTime'] = pd.to_datetime(unicode(row['EndTime']))
		except ValueError:
			continue

		if row['StartTime'] > row['EndTime']:
			print 'ERROR: start time after end time in', root, filename
			print row


			


def main(rootdir):
	# walk directory to find parse annotation csv files
     print 'checking files....'
     for root, dirs, files in os.walk(rootdir):
        for filename in files:
            if filename.endswith('.csv'):
                f = os.path.join(root,filename)

                csv_file = open(f, 'r')
                data = pd.read_csv(csv_file, parse_dates=True)
                check_valid_time(data, root, filename)
                check_time_interval(data, root, filename)


if __name__ == '__main__':
	rootdir = '/Users/knuth/Documents/ooi/repos/github/annotations/annotations/RS03AXPS'
	main(rootdir)
