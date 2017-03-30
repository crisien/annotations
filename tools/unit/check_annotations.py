import os
import pandas as pd





def check_dups(data, root, filename):
	dups = data[data.duplicated(keep=False)]
	if not dups.empty == True:
		print 'WARNING: duplicate annotations in', root, filename
		print dups



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
			print 'WARNING: start time after end time in', root, filename
			print row


def check_annotation_interval(data, root, filename):
	row_iterator = data.iterrows()
	_, last = row_iterator.next()
	for index, row in row_iterator:
		try:
			row['StartTime'] = pd.to_datetime(unicode(row['StartTime']))
			row['EndTime'] = pd.to_datetime(unicode(row['EndTime']))
			last['StartTime'] = pd.to_datetime(unicode(last['StartTime']))
			last['EndTime'] = pd.to_datetime(unicode(last['EndTime']))

			diff = row['StartTime'] - last['EndTime']
			# if row['Status'] == last['Status'] and row['Deployment'] == last['Deployment'] and diff < pd.Timedelta('1 second'):
			if row['Status'] == last['Status'] and row['Deployment'] == last['Deployment'] and row['StartTime'] != last['EndTime']:
				print 'WARNING: end time of row ' + str(index + 1) + ' is not equal to the begin time of row ' + str(index + 2)
				print 'there is an unidentified gap of ' + str(diff) + ' between annotations with the same status'

			if row['Status'] == last['Status'] and row['Deployment'] == last['Deployment'] and row['StartTime'] == last['EndTime']:
				print 'WARNING: end time of row ' + str(index + 1) + ' is equal to the begin time of row ' + str(index + 2)
				print 'these annotations have the same status and should be merged'

			last = row

		except ValueError:
			continue


def check_valid_time(data, root, filename):
	# iterate over start and end times
	for index, row in data.iterrows():
		try:
			row['StartTime'] = pd.to_datetime(unicode(row['StartTime']))
		except ValueError as ve:
			print 'WARNING:', ve, 'in', root, filename
			print row

		try:
			row['EndTime'] = pd.to_datetime(unicode(row['EndTime']))
		except ValueError as ve:
			print 'WARNING:', ve, 'in', root, filename
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
                check_dups(data, root, filename)
                check_annotation_interval(data, root, filename)


if __name__ == '__main__':
	rootdir = '/Users/knuth/Documents/ooi/repos/github/annotations/test/annotations/RS03AXPS/RS03AXPS-SF03A-2A-CTDPFA302'
	main(rootdir)
