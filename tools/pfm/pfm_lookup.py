import pandas as pd
import yaml


f = '/Users/knuth/Documents/ooi/repos/github/annotations/tools/pfm/all_params.csv'
ref_des = 'RS03AXPS-PC03A-4A-CTDPFA303'
pd_number = 'PD194'



csv_file = open(f, 'r')
data = pd.read_csv(csv_file, parse_dates=True)


# reduce data frame to relevant columns
columns = ['reference_designator','start_depth','end_depth','method','stream_name', 'parameter_id',
							'name.1','parameter_function_map', 'data_product_identifier', 'data_level']
data = data[columns]
affected_PDs = []


def pfm_check(possible_instruments, pd_number):
	for index, row in possible_instruments.iterrows():
		try:	
			if pd_number in row['parameter_function_map']:
				# print pd_number, 'is contained within', row['reference_designator'], row['stream_name'], row['name.1'], 'with PD' + str(int(row['parameter_id']))
				text = row['reference_designator'] + ' ' + row['stream_name'] + ' ' + row['name.1'] + ' ' +  'PD' + str(int(row['parameter_id']))
				next_pd = 'PD' + str(int(row['parameter_id']))
				affected_PDs.append(text)
				pfm_check(possible_instruments, next_pd)
		except TypeError:
			continue


def node_check(data):
	# subset data to node level
	instruments_on_node = []
	for index, row in data.iterrows():
		if ref_des[9:14] in row['reference_designator'][9:14]:
			instruments_on_node.append(row)
	instruments_on_node = pd.DataFrame(instruments_on_node)
	return instruments_on_node



possible_instruments = node_check(data)
pfm_check(possible_instruments, pd_number)
affected_PDs = set(affected_PDs)


print '\nThe following PD numbers are affected and need annotation:\n'
for i in affected_PDs:
	print i






