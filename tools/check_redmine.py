import os
import pandas as pd
import re
import numpy as np


def find_redmine_tickets(data, root, filename):
	# iterate over start and end times
	for index, row in data.iterrows():
		try:
			return int(row['Redmine#'])
		except:
			continue


def main(rootdir):
	# walk directory to find parse annotation csv files
     redmines = []
     for root, dirs, files in os.walk(rootdir):
        for filename in files:
            if filename.endswith('.csv'):
                f = os.path.join(root,filename)
                csv_file = open(f, 'r')
                data = pd.read_csv(csv_file, na_values=['nan'], keep_default_na=False)
                return_f = find_redmine_tickets(data, root, filename)
                redmines.append(return_f)
     for i in set(redmines):
     	if i != None:
     		print i


if __name__ == '__main__':
	rootdir = '/Users/knuth/Documents/ooi/repos/github/annotations/annotations'
	main(rootdir)