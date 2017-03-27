import pandas as pd
import os



def buoy_check(data, ref_des, method):
	instruments_on_node = []
	for index, row in data.iterrows():
		if ref_des[:8] in row['reference_designator'][:8] and row['method'] == method:
			instruments_on_node.append(row)
	instruments_on_node = pd.DataFrame(instruments_on_node)
	return instruments_on_node


def fix_trailing_newline(fname):
    with open(fname, "r+") as f:
        f.seek(-1, 2)
        if(f.read() != '\n'):
            f.seek(0, 2)
            f.write('\n')


def node_check(data, ref_des, method):
	# subset data to node level
	instruments_on_node = []
	for index, row in data.iterrows():
		if ref_des[9:14] in row['reference_designator'][9:14] and row['method'] == method:
			instruments_on_node.append(row)
	instruments_on_node = pd.DataFrame(instruments_on_node)
	return instruments_on_node



def make_dir(save_dir):
    try:  # Check if the save_dir exists already... if not, make it
        os.mkdir(save_dir)
    except OSError:
        pass



def pfm_check(possible_instruments, pd_number, affected_PDs):
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