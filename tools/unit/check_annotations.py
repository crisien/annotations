import os
import pandas as pd
import re
import numpy as np


# specify regular expression to identify specific csv types for parsing
delivery_methods = ['streamed', 'recovered_host', 'telemetered', 'recovered_inst', 'recovered_cspp', 'streamed', 'recovered_wfp']
dm_reg_ex = re.compile('|'.join(delivery_methods))
params_csv_name = ['parameters']
p_reg_ex = re.compile('|'.join(params_csv_name))



def check_dups(data, root, filename):
	dups = data[data.duplicated(keep=False)]
	if not dups.empty == True:
		print '\n', root, filename
		print 'WARNING: duplicate annotations in rows ' + str(dups.index.values[1]+1) + ' and ' + str(dups.index.values[1]+2)
		return True



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
			print '\n', root, filename
			print 'WARNING: start time after end time in row ' + str(index + 2)
			return True



def check_annotation_gap(data, root, filename):
	if dm_reg_ex.search(filename) and not p_reg_ex.search(filename):
		try:
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
					if row['Deployment'] == last['Deployment'] and row['StartTime'] != last['EndTime'] and row['Status'] is not np.nan:
						print '\n', root, filename
						print 'WARNING: there is an unidentified annotation gap of ' + str(diff) + \
						' between deployment ' + str(row['Deployment']) + ' annotations in row ' + \
						str(index + 1) + ' and row ' + str(index + 2)

					last = row

				except ValueError:
					continue
		except StopIteration:
			pass


def check_annotation_interval(data, root, filename):
	if dm_reg_ex.search(filename) and not p_reg_ex.search(filename):
		try:
			row_iterator = data.iterrows()
			_, last = row_iterator.next()
			for index, row in row_iterator:
				try:
					row['StartTime'] = pd.to_datetime(unicode(row['StartTime']))
					row['EndTime'] = pd.to_datetime(unicode(row['EndTime']))
					last['StartTime'] = pd.to_datetime(unicode(last['StartTime']))
					last['EndTime'] = pd.to_datetime(unicode(last['EndTime']))	

					if row['Status'] == last['Status'] and row['Deployment'] == last['Deployment'] and row['StartTime'] == last['EndTime']:
						print '\n', root, filename
						print 'WARNING: end time of row ' + str(index + 1) + ' is equal to the begin time of row ' + str(index + 2) + \
						'. these annotations are from the same deployment, have the same status and should be merged'

					last = row

				except ValueError:
					continue
		except StopIteration:
			pass


def check_valid_time(data, root, filename):
	# iterate over start and end times
	for index, row in data.iterrows():
		try:
			row['StartTime'] = pd.to_datetime(unicode(row['StartTime']))
		except ValueError as ve:
			print '\n', root, filename
			print 'WARNING:', ve, 'in row ' + str(index + 2) + ". can't convert timestamp"
		    # print row

		try:
			row['EndTime'] = pd.to_datetime(unicode(row['EndTime']))
		except ValueError as ve:
			print '\n', root, filename
			print 'WARNING:', ve, 'in row ' + str(index + 2) + ". can't convert timestamp"
			# print row



def main(rootdir):
	# walk directory to find parse annotation csv files
     print 'checking files....'
     for root, dirs, files in os.walk(rootdir):
		 dirs[:] = [d for d in dirs if d not in "internal_drafts" and d not in "internal_notes"]
		 for filename in files:
				if filename.endswith('.csv'):
					f = os.path.join(root,filename)
					# print f
					csv_file = open(f, 'r')
					data = pd.read_csv(csv_file, parse_dates=True)
					check_valid_time(data, root, filename)
					check_time_interval(data, root, filename)
					check_dups(data, root, filename)
					check_annotation_gap(data, root, filename)
					check_annotation_interval(data, root, filename)
		 # print '\n'

                


if __name__ == '__main__':
	rootdir = '/Users/knuth/Documents/ooi/repos/github/annotations/annotations'
	main(rootdir)
