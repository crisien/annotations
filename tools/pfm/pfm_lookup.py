import pandas as pd
import re

# define your inputs
f = '/Users/knuth/Documents/ooi/repos/github/annotations/tools/pfm/all_params.csv'

# ref_des = 'RS03AXPS-PC03A-4A-CTDPFA303'
# stream = 'ctdpf_optode_sample'
# method = 'streamed' # 'recovered_host' 'telemetered' 'recovered_inst' 'recovered_cspp' 'streamed' 'recovered_wfp'
# pd_number = 'PD194'

# ref_des = 'CE02SHSM-RID27-03-CTDBPC000'
# stream = 'ctdbp_cdef_instrument_recovered'
# method = 'recovered_inst' # 'recovered_host' 'telemetered' 'recovered_inst' 'recovered_cspp' 'streamed' 'recovered_wfp'
# pd_number = 'PD923'

ref_des = 'CE02SHSM-RID27-03-CTDBPC000'
stream = 'ctdbp_cdef_dcl_instrument'
method = 'telemetered' # 'recovered_host' 'telemetered' 'recovered_inst' 'recovered_cspp' 'streamed' 'recovered_wfp'
pd_number = 'PD923'

# ref_des = 'CE02SHSM-RID27-03-CTDBPC000'
# stream = 'ctdbp_cdef_dcl_instrument_recovered'
# method = 'recovered_host' # 'recovered_host' 'telemetered' 'recovered_inst' 'recovered_cspp' 'streamed' 'recovered_wfp'
# pd_number = 'PD923'


def buoy_check(data):
	instruments_on_node = []
	for index, row in data.iterrows():
		if ref_des[:8] in row['reference_designator'][:8] and row['method'] == method:
			instruments_on_node.append(row)
	instruments_on_node = pd.DataFrame(instruments_on_node)
	return instruments_on_node



def node_check(data):
	# subset data to node level
	instruments_on_node = []
	for index, row in data.iterrows():
		if ref_des[9:14] in row['reference_designator'][9:14] and row['method'] == method:
			instruments_on_node.append(row)
	instruments_on_node = pd.DataFrame(instruments_on_node)
	return instruments_on_node



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



# read in data
csv_file = open(f, 'r')
data = pd.read_csv(csv_file, parse_dates=True)

# reduce data frame to relevant columns
columns = ['reference_designator','start_depth','end_depth','method','stream_name', 'parameter_id',
							'name.1','parameter_function_map', 'data_product_identifier', 'data_level']
data = data[columns]

# stage list of expected PD numbers to br printed from at end of script
affected_PDs = []

# create regular expression to enter buoy exception and search across nodes
buoy_nodes = ['RID', 'SBD']
reg_ex = re.compile('|'.join(buoy_nodes))

# further reduce data frame to only those instruments that might be affected
if reg_ex.search(ref_des):
	possible_instruments = buoy_check(data)
else:
	possible_instruments = node_check(data)

# begin recursive search on reduced data frame
pfm_check(possible_instruments, pd_number)
affected_PDs = set(affected_PDs)

# print output
print '\nThe following PD numbers use ' + pd_number + ' from ' + ref_des + '-' + stream + \
		' and may need annotation:\n'
for i in affected_PDs:
	print i






