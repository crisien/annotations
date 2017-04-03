import os
import pandas as pd
import re
import numpy as np


def find_redmine_tickets(data, root, filename):
    # iterate over start and end times
    file_redmine_list = []
    for index, row in data.iterrows():
        try:
            # print int(row['Redmine#'])
            x = int(row['Redmine#'])
            file_redmine_list.append(x)
        except:
            continue
    return file_redmine_list


def main(rootdir):
    # walk directory to find parse annotation csv files
    redmine_list = []
    for root, dirs, files in os.walk(rootdir):
        for filename in files:
            if filename.endswith('.csv'):
                f = os.path.join(root,filename)
                csv_file = open(f, 'r')
                data = pd.read_csv(csv_file, na_values=['nan'], keep_default_na=False)
                x = find_redmine_tickets(data, root, filename)
                redmine_list.extend(x)
    print set(redmine_list)



if __name__ == '__main__':
    rootdir = '/Users/knuth/Documents/ooi/repos/github/annotations/annotations'
    main(rootdir)