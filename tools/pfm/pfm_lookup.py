import pandas as pd
from functions.functions import *
import re
import os
import csv


def main(	QC_database_export, annotations_dir, ref_des, stream, method, pd_number, 
			write_annotation_csv, parameter_name, deployment, start_time,
			end_time, annotation_pd, annotation_affected, status, reviewed_by):
	

	annotation_headers = ['Level', 'Deployment', 'StartTime', 'EndTime', 'Annotation', 'Status',
                                       'Redmine#', 'Todo', 'reviewed_by']
	# make annotation dirs if they don't already exists
	subsite = ref_des[:8]
	subsite_dir = os.path.join(annotations_dir, subsite)
	
	make_dir(subsite_dir)

	refdes_dir = os.path.join(subsite_dir, ref_des)
	make_dir(refdes_dir)


	# specify output annotation csv files
	if write_annotation_csv == True:
		# subsite_file = os.path.join(subsite_dir + '.csv')
		# stream_file = os.path.join(refdes_dir + stream + '.csv')
		params_file = os.path.join(refdes_dir + '/' + stream + '-parameters.csv')
		source_annotation = (parameter_name, deployment, start_time, end_time, annotation_pd, status, '', '', reviewed_by)
		print params_file
		with open(params_file,'a') as params_a_csv:
			writer = csv.writer(params_a_csv)
			if os.stat(params_file).st_size==0:
				writer.writerow(annotation_headers)
				writer.writerow(source_annotation)
			else:
				writer.writerow(source_annotation)
			

	# read in data
	csv_file = open(QC_database_export, 'r')
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
		possible_instruments = buoy_check(data, ref_des, method)
	else:
		possible_instruments = node_check(data, ref_des, method)

	# begin recursive search on reduced data frame
	pfm_check(possible_instruments, pd_number, affected_PDs)
	affected_PDs = list(set(affected_PDs))

	# print output
	print '\n' + pd_number + ' from ' + ref_des + '-' + stream + ' is to calculate:\n'
	for i in affected_PDs:
		print i
	print '\n'
	affected_PDs = pd.DataFrame(affected_PDs)
	# print type(affected_PDs)

	if write_annotation_csv == True:
		# write out parameter annotations
		with open(params_file,'a') as params_a_csv:
			writer = csv.writer(params_a_csv)
			for i in affected_PDs:
				print i
				# newline = (i[0])
				# writer.writerow(newline)


if __name__ == '__main__':
	# define your inputs and run the test to check the outputs in terminal. Se write annotation csv to False
	QC_database_export = '/Users/knuth/Documents/ooi/repos/github/annotations/tools/pfm/all_params.csv'
	annotations_dir = '/Users/knuth/Documents/ooi/repos/github/annotations/annotations'
	ref_des = 'CE02SHSM-RID27-03-CTDBPC000'
	stream = 'ctdbp_cdef_dcl_instrument'
	method = 'telemetered' # 'recovered_host' 'telemetered' 'recovered_inst' 'recovered_cspp' 'streamed' 'recovered_wfp'
	pd_number = 'PD923'


	# if the identified pds check out as being affected, specify the following inputs to generate the annotations
	write_annotation_csv = False
	parameter_name = 'salinity'
	deployment = '1'
	start_time = 'test'
	end_time = 'test'
	annotation_pd = 'test'
	annotation_affected = 'test'
	status = 'test'
	reviewed_by = 'test'




	main(	QC_database_export, 
			annotations_dir, 
			ref_des, 
			stream, 
			method, 
			pd_number, 
			write_annotation_csv,
			parameter_name,
			deployment,
			start_time,
			end_time,
			annotation_pd,
			annotation_affected,
			status,
			reviewed_by
		)







	# ref_des = 'RS03AXPS-PC03A-4A-CTDPFA303'
	# stream = 'ctdpf_optode_sample'
	# method = 'streamed' # 'recovered_host' 'telemetered' 'recovered_inst' 'recovered_cspp' 'streamed' 'recovered_wfp'
	# pd_number = 'PD194'

	# ref_des = 'CE02SHSM-RID27-03-CTDBPC000'
	# stream = 'ctdbp_cdef_instrument_recovered'
	# method = 'recovered_inst' # 'recovered_host' 'telemetered' 'recovered_inst' 'recovered_cspp' 'streamed' 'recovered_wfp'
	# pd_number = 'PD923'


	# ref_des = 'CE02SHSM-RID27-03-CTDBPC000'
	# stream = 'ctdbp_cdef_dcl_instrument_recovered'
	# method = 'recovered_host' # 'recovered_host' 'telemetered' 'recovered_inst' 'recovered_cspp' 'streamed' 'recovered_wfp'
	# pd_number = 'PD923'

