#!/usr/bin/env python

import requests
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# TODO auto source deployment time ranges
# TODO create color legend
# TODO calculate metrics

# specify path to annotation csvs, reference designator and theoretical end date for ongoing deployment, specified as 'None' in asset management
# (you can use the date on which you downloaded the data, for example.)
assets = '/Users/knuth/Documents/ooi/repos/github/annotations/annotations/RS03AXPS/RS03AXPS.csv'
stream = '/Users/knuth/Documents/ooi/repos/github/annotations/annotations/RS03AXPS/RS03AXPS-SF03A-2A-CTDPFA302/streamed-ctdpf_sbe43_sample.csv'
parameters = '/Users/knuth/Documents/ooi/repos/github/annotations/annotations/RS03AXPS/RS03AXPS-SF03A-2A-CTDPFA302/streamed-ctdpf_sbe43_sample-parameters.csv'
reference_designator = 'RS03AXPS-SF03A-2A-CTDPFA302'
ongoing_dep_end = '2017-03-21T00:00:00'

## use this to manually specify deployment start and end times. comment block using ongoing_dep_end out accordingly.
# deployments_df = pd.DataFrame([['2014-09-27T18:33:00','2015-07-09T00:00:00'],['2015-07-09T04:16:00','2016-07-14T00:00:00'], ['2016-07-14T21:18:00','2017-03-21T00:00:00']])


def request_qc_json(ref_des):
    url = 'http://ooi.visualocean.net/instruments/view/'
    ref_des_url = os.path.join(url, ref_des)
    ref_des_url += '.json'
    data = requests.get(ref_des_url).json()
    return data

def get_deployment_information(data):
    d_info = [x for x in data['instrument']['deployments']]
    if d_info:
        return d_info
    else:
        return None


dep_data = request_qc_json(reference_designator)
deploy_info = get_deployment_information(dep_data)
deployments_df = pd.DataFrame(deploy_info)
deployments_df = deployments_df[['start_date', 'stop_date']]
deployments_df.fillna(value=ongoing_dep_end, inplace=True)





# read in csv files
assets_df = pd.read_csv(assets, parse_dates=True)
stream_df = pd.read_csv(stream, parse_dates=True)
parameters_df = pd.read_csv(parameters, parse_dates=True)





# output all annotations to single csv for report
df = assets_df
df = df.append(stream_df)
df = df.append(parameters_df)
df.to_csv(open('annotations_list.csv', 'w'))




# convert time stamps to date time
deployments_df['start_date'] = deployments_df['start_date'].apply(lambda x: pd.to_datetime(unicode(x)))
deployments_df['stop_date'] = deployments_df['stop_date'].apply(lambda x: pd.to_datetime(unicode(x)))


assets_df['StartTime'] = assets_df['StartTime'].apply(lambda x: pd.to_datetime(unicode(x)))
assets_df['EndTime'] = assets_df['EndTime'].apply(lambda x: pd.to_datetime(unicode(x)))

stream_df['StartTime'] = stream_df['StartTime'].apply(lambda x: pd.to_datetime(unicode(x)))
stream_df['EndTime'] = stream_df['EndTime'].apply(lambda x: pd.to_datetime(unicode(x)))

parameters_df['StartTime'] = parameters_df['StartTime'].apply(lambda x: pd.to_datetime(unicode(x)))
parameters_df['EndTime'] = parameters_df['EndTime'].apply(lambda x: pd.to_datetime(unicode(x)))





# create timeline labels and indices
yticks = ['Deployments']

for index, row in assets_df.iterrows():
	if len(row["Level"]) == 8:
		yticks.append(row["Level"])
for index, row in assets_df.iterrows():
	if len(row["Level"]) == 14:
		yticks.append(row["Level"])
for index, row in assets_df.iterrows():
	if len(row["Level"]) == 27 and row["Level"] == reference_designator:
		yticks.append(row["Level"])

for index, row in stream_df.iterrows():
	yticks.append(row["Level"])

for index, row in parameters_df.iterrows():
	yticks.append(row["Level"])

yticks = pd.unique(yticks)
yticks = yticks[::-1]
y = np.arange(len(yticks))
counter = -1






# plot deployment timelines
for index, row in deployments_df.iterrows():
	deploy_time = np.array([row[0],row[1]])
	deploy_shape = np.full((deploy_time.shape), y[counter])
	plt.plot(deploy_time, deploy_shape, linewidth=10, color='blue')

counter = counter -1




# plot subsite timelines
for index, row in stream_df.iterrows():
	stream_time = np.array([row["StartTime"],row["EndTime"]])
	stream_shape = np.full((stream_time.shape), y[counter])
	# TODO available timeline shows inaccurate overlap
	if row["Status"] == 'AVAILABLE':
		plt.plot(stream_time, stream_shape, linewidth=10, color='green')
	elif row["Status"] == 'NOT_AVAILABLE':
		plt.plot(stream_time, stream_shape, linewidth=10, color='green')
	elif row["Status"] == 'NOT_EVALUATED':
		plt.plot(stream_time, stream_shape, linewidth=10, color='green')
	elif row["Status"] == 'PENDING_INGEST':
		plt.plot(stream_time, stream_shape, linewidth=10, color='green',zorder = 3)

for index, row in assets_df.iterrows():
	subsite_time = np.array([row["StartTime"],row["EndTime"]])
	subsite_shape = np.full((subsite_time.shape), y[counter])
	if len(row["Level"]) == 8 and type(row["Status"]) == str:
		plt.plot(subsite_time, subsite_shape, linewidth=10, color='gray',zorder = 3)

counter = counter -1





# plot node timelines
for index, row in stream_df.iterrows():
	stream_time = np.array([row["StartTime"],row["EndTime"]])
	stream_shape = np.full((stream_time.shape), y[counter])
	# TODO available timeline shows inaccurate overlap
	if row["Status"] == 'AVAILABLE':
		plt.plot(stream_time, stream_shape, linewidth=10, color='green')
	elif row["Status"] == 'NOT_AVAILABLE':
		plt.plot(stream_time, stream_shape, linewidth=10, color='green')
	elif row["Status"] == 'NOT_EVALUATED':
		plt.plot(stream_time, stream_shape, linewidth=10, color='green')
	elif row["Status"] == 'PENDING_INGEST':
		plt.plot(stream_time, stream_shape, linewidth=10, color='lightgray',zorder = 3)

for index, row in assets_df.iterrows():
	subsite_time = np.array([row["StartTime"],row["EndTime"]])
	subsite_shape = np.full((subsite_time.shape), y[counter])
	if len(row["Level"]) == 8 and type(row["Status"]) == str:
		plt.plot(subsite_time, subsite_shape, linewidth=10, color='gray',zorder = 3)

for index, row in assets_df.iterrows():
	node_time = np.array([row["StartTime"],row["EndTime"]])
	node_shape = np.full((node_time.shape), y[counter])
	if len(row["Level"]) == 14 and type(row["Status"]) == str:
		plt.plot(node_time, node_shape, linewidth=10, color='gray',zorder = 3)

counter = counter -1





# plot instrument timelines
for index, row in stream_df.iterrows():
	stream_time = np.array([row["StartTime"],row["EndTime"]])
	stream_shape = np.full((stream_time.shape), y[counter])
	# TODO available timeline shows inaccurate overlap
	if row["Status"] == 'AVAILABLE':
		plt.plot(stream_time, stream_shape, linewidth=10, color='green')
	elif row["Status"] == 'NOT_AVAILABLE':
		plt.plot(stream_time, stream_shape, linewidth=10, color='gray',zorder = 3)
	elif row["Status"] == 'NOT_EVALUATED':
		plt.plot(stream_time, stream_shape, linewidth=10, color='green')
	elif row["Status"] == 'PENDING_INGEST':
		plt.plot(stream_time, stream_shape, linewidth=10, color='lightgray',zorder = 3)

for index, row in assets_df.iterrows():
	subsite_time = np.array([row["StartTime"],row["EndTime"]])
	subsite_shape = np.full((subsite_time.shape), y[counter])
	if len(row["Level"]) == 8 and type(row["Status"]) == str:
		plt.plot(subsite_time, subsite_shape, linewidth=10, color='gray',zorder = 3)

for index, row in assets_df.iterrows():
	node_time = np.array([row["StartTime"],row["EndTime"]])
	node_shape = np.full((node_time.shape), y[counter])
	if len(row["Level"]) == 14 and type(row["Status"]) == str:
		plt.plot(node_time, node_shape, linewidth=10, color='gray',zorder = 3)

for index, row in assets_df.iterrows():
	instrument_time = np.array([row["StartTime"],row["EndTime"]])
	instrument_shape = np.full((instrument_time.shape), y[counter])
	if len(row["Level"]) == 27 and type(row["Status"]) == str and row["Level"]=='reference_designator':
		plt.plot(instrument_time, instrument_shape, linewidth=10, color='gray',zorder = 3)

counter = counter -1





# plot stream timelines
for index, row in stream_df.iterrows():
	stream_time = np.array([row["StartTime"],row["EndTime"]])
	stream_shape = np.full((stream_time.shape), y[counter])
	if row["Status"] == 'AVAILABLE':
		plt.plot(stream_time, stream_shape, linewidth=10, color='green')
	elif row["Status"] == 'NOT_AVAILABLE':
		plt.plot(stream_time, stream_shape, linewidth=10, color='gray',zorder = 3)
	elif row["Status"] == 'NOT_EVALUATED':
		plt.plot(stream_time, stream_shape, linewidth=10, color='steelblue',zorder = 3)
	elif row["Status"] == 'PENDING_INGEST':
		plt.plot(stream_time, stream_shape, linewidth=10, color='lightgray',zorder = 3)
counter = counter -1




# plot parameter timelines
parameters = yticks[:-5]
parameters = parameters[::-1]

for parameter in parameters:
	for index, row in stream_df.iterrows():
		stream_time = np.array([row["StartTime"],row["EndTime"]])
		stream_shape = np.full((stream_time.shape), y[counter])
		if row["Status"] == 'AVAILABLE':
			plt.plot(stream_time, stream_shape, linewidth=10, color='green')
		elif row["Status"] == 'NOT_AVAILABLE':
			plt.plot(stream_time, stream_shape, linewidth=10, color='gray',zorder = 3)
		elif row["Status"] == 'NOT_EVALUATED':
			plt.plot(stream_time, stream_shape, linewidth=10, color='steelblue',zorder = 3)
		elif row["Status"] == 'PENDING_INGEST':
			plt.plot(stream_time, stream_shape, linewidth=10, color='lightgray',zorder = 3)

	for index, row in parameters_df.iterrows():
		if row["Level"] == parameter:
			parameter_time = np.array([row["StartTime"],row["EndTime"]])
			parameter_shape = np.full((parameter_time.shape), y[counter])
			if row["Status"] == 'SUSPECT':
				plt.plot(parameter_time, parameter_shape, linewidth=10, color='orange')
			elif row["Status"] == 'FAIL':
				plt.plot(parameter_time, parameter_shape, linewidth=10, color='red')
	counter = counter -1




# show plot
plt.title(reference_designator)
plt.yticks(y, yticks)
plt.xticks(rotation=20)
plt.tight_layout()
plt.ylim([-1,len(yticks)])
plt.grid()
plt.show()

