import pandas as pd
from functions.functions import *
import re
import os
import csv
import subprocess


# TODO add check for duplicate records in annotations csv and purge

def main(	QC_database_export, annotations_dir, ref_des, stream, method, pd_number, DPI,
			write_annotation_csv, parameter_name, deployment, start_time,
			end_time, annotation_pd, annotation_affected, status, reviewed_by):
	

	annotation_headers = ['Level', 'Deployment', 'StartTime', 'EndTime', 'Annotation', 'Status',
                                       'Redmine#', 'Todo', 'reviewed_by']
	
	# make annotation dirs if they don't already exists
	if write_annotation_csv == True:
		subsite = ref_des[:8]
		subsite_dir = os.path.join(annotations_dir, subsite)
		
		make_dir(subsite_dir)

		refdes_dir = os.path.join(subsite_dir, ref_des)
		make_dir(refdes_dir)


	# specify output annotation csv files
	if write_annotation_csv == True:
		# subsite_file = os.path.join(subsite_dir + '.csv')
		# stream_file = os.path.join(refdes_dir + stream + '.csv')
		params_file = os.path.join(refdes_dir + '/'  + method + '-'+ stream + '-parameters.csv')
		source_annotation = (parameter_name, deployment, start_time, end_time, annotation_pd, status, '', '', reviewed_by)
		
		try:
			os.stat(params_file).st_size==0
		except:
			with open(params_file,'w') as params_a_csv:
				writer = csv.writer(params_a_csv)
				fieldnames = annotation_headers
				writer = csv.DictWriter(params_a_csv, fieldnames=fieldnames)
				writer.writeheader()
				print 'creating ' + params_file


		fix_trailing_newline(params_file)


		with open(params_file,'a') as params_a_csv:
			writer = csv.writer(params_a_csv)
			writer.writerow(source_annotation)
			print 'appending source annotation for ' + parameter_name + ' to ' + ref_des + '/' + method + '-'+ stream + '-parameters.csv'


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

	# begin recursive search on reduced data frame and append to affected_PDs list
	pfm_check(possible_instruments, pd_number, DPI, affected_PDs)
	affected_PDs = list(set(affected_PDs))

	params_file_t = ''
	if write_annotation_csv == True:
		# write out target parameter annotations
		# create dirs and parameter level csv files, unless they already exist

		for i in affected_PDs:
			i = i.split()

			subsite_t = i[0][:8]
			subsite_dir_t = os.path.join(annotations_dir, subsite_t)
			make_dir(subsite_dir_t)
			ref_des_t = i[0][:27]
			refdes_dir_t = os.path.join(subsite_dir_t, ref_des_t)
			make_dir(refdes_dir_t)
			params_file_t = os.path.join(refdes_dir_t + '/'  + method + '-'+ i[1] + '-parameters.csv')

			# subprocess.call(["dos2unix", params_file_t])

			try:
				os.stat(params_file_t).st_size==0
			except:
				with open(params_file_t,'w') as params_a_csv_t:
					fieldnames = annotation_headers
					writer_h = csv.DictWriter(params_a_csv_t, fieldnames=fieldnames)
					writer_h.writeheader()
					print 'creating ' + params_file_t
				
		print '\n'
		# append info to parameter level csv files
		for i in affected_PDs:
			i = i.split()

			subsite_t = i[0][:8]
			subsite_dir_t = os.path.join(annotations_dir, subsite_t)
			ref_des_t = i[0][:27]
			refdes_dir_t = os.path.join(subsite_dir_t, ref_des_t)
			params_file_t = os.path.join(refdes_dir_t + '/'  + method + '-'+ i[1] + '-parameters.csv')

			fix_trailing_newline(params_file_t)


			with open(params_file_t,'a') as params_a_csv_t:
				writer_t = csv.writer(params_a_csv_t)
				target_annotation = (i[2], deployment, start_time, end_time, annotation_affected, status, '', '', reviewed_by)
				writer_t.writerow(target_annotation)
				print 'appending target annotation for ' + i[2] + ' to ' + ref_des_t + '/' + method + '-'+ i[1] + '-parameters.csv'



	else:
		print '\n' + pd_number + ' from ' + ref_des + ' ' + method + '-' + stream + ' is used to calculate:\n'
		for i in affected_PDs:
			print i
		print '\n'


if __name__ == '__main__':
	# define your inputs and run the test to check the outputs in terminal. Set write annotation csv to False
	QC_database_export = '/Users/knuth/Documents/ooi/repos/github/annotations/tools/pfm/all_params.csv'
	annotations_dir = '/Users/knuth/Documents/ooi/repos/github/annotations/test'
	ref_des = 'RS03AXPS-SF03A-2A-CTDPFA302'
	stream = 'ctdpf_sbe43_sample'
	method = 'streamed' # 'recovered_host' 'telemetered' 'recovered_inst' 'recovered_cspp' 'streamed' 'recovered_wfp'
	pd_number = 'PD194'
	DPI = 'CONDWAT_L0'


	# if the identified pds check out as being affected, specify the following inputs to generate the annotations
	write_annotation_csv = False
	parameter_name = 'conductivity'
	deployment = '2'
	start_time = '2017-01-12T13:00:00'
	end_time = '2017-01-12T17:00:00'
	annotation_pd = 'Data values are within plausible ranges, but lower than usual L0 conductivity values throughout the entire water column during this time period make the values suspect.'
	annotation_affected = 'Data values are within plausible ranges, but lower than usual L0 conductivity values throughout the entire water column during this time period make the values suspect.'
	status = 'SUSPECT'
	reviewed_by = 'friedrich'




	main(	QC_database_export, 
			annotations_dir, 
			ref_des, 
			stream, 
			method, 
			pd_number,
			DPI, 
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

