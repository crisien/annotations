import pandas as pd
import os



def buoy_check(data, ref_des, method):
	print 'WARNING: buoy_check function is not ready yet'
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



def pfm_check(possible_instruments, pd_number, DPI, affected_PDs):
	for index, row in possible_instruments.iterrows():
		try:	
			if pd_number in row['parameter_function_map'] or DPI in row['parameter_function_map']:
				# print pd_number, 'is contained within', row['reference_designator'], row['stream_name'], row['name.1'], 'with PD' + str(int(row['parameter_id']))
				text = row['reference_designator'] + ' ' + row['stream_name'] + ' ' + row['name.1'] + ' ' +  'PD' + str(int(row['parameter_id']))
				next_pd = 'PD' + str(int(row['parameter_id']))
				next_DPI = str(row['data_product_identifier'])
				affected_PDs.append(text)
				pfm_check(possible_instruments, next_pd, next_DPI, affected_PDs)
		except TypeError:
			continue



# TODO improve buoy check. From Pete:

'''
https://uframe-cm.ooi.rutgers.edu/issues/12102#note-3
DOSTA, NUTNR, OPTAA and FLORT on the surface buoy use the METBK data


for every other instrument in the system the co-located CTD is either a) on the same node or b) on a different node but at the exact same depth

for example:

CE02SHSM-RID26-00-DCLENG000,7.0
CE02SHSM-RID26-01-ADCPTA000,7.0
CE02SHSM-RID26-04-VELPTA000,7.0
CE02SHSM-RID26-06-PHSEND000,7.0
CE02SHSM-RID26-07-NUTNRB000,7.0
CE02SHSM-RID26-08-SPKIRB000,7.0
CE02SHSM-RID27-00-DCLENG000,7.0
CE02SHSM-RID27-01-OPTAAD000,7.0
CE02SHSM-RID27-02-FLORTD000,7.0
CE02SHSM-RID27-03-CTDBPC000,7.0
CE02SHSM-RID27-04-DOSTAD000,7.0
 
the CTD is on RID27 but serves instruments on RID26 and RID27
'''