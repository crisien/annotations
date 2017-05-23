#!/usr/bin/env python
import requests
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


# specify path to annotation csvs and reference designator reviewed
assets = '/Users/knuth/Documents/ooi/repos/github/annotations/annotations/GA03FLMA/GA03FLMA.csv'
stream = '/Users/knuth/Documents/ooi/repos/github/annotations/annotations/GA03FLMA/GA03FLMA-RIM01-02-CTDMOH051/telemetered-ctdmo_ghqr_sio_mule_instrument.csv'
parameters = '/Users/knuth/Documents/ooi/repos/github/annotations/annotations/GA03FLMA/GA03FLMA-RIM01-02-CTDMOH051/telemetered-ctdmo_ghqr_sio_mule_instrument-parameters.csv'
reference_designator = 'GA03FLMA-RIM01-02-CTDMOG051'


# read in csv files
assets_df = pd.read_csv(assets, parse_dates=True)
stream_df = pd.read_csv(stream, parse_dates=True)
parameters_df = pd.read_csv(parameters, parse_dates=True)


# grab subsite and node from specified reference designator
subsite_name = reference_designator[0:8]
node_name = reference_designator[0:14]


# output all annotations to single csv for report
df = assets_df
df = df[(df.Level == subsite_name) | (df.Level == node_name) | (df.Level == reference_designator)]
df = df.append(stream_df)
df = df.append(parameters_df)
df = df[df.Status != 'AVAILABLE']
df = df[df.StartTime.notnull()]
df = df.drop(df.columns[[7, 8, 9]], axis=1)
columns = df.columns
columns = [str(x) for x in columns.tolist()]
df = df.sort([columns[2],columns[3]], ascending=[1,1])
df.to_csv(open('annotations_list.csv', 'w'),columns=columns, index=False)



# convert time stamps to date time
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
	if len(row["Level"]) == 14 and row["Level"] == node_name:
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
for index, row in stream_df.iterrows():
	stream_time = np.array([row["StartTime"],row["EndTime"]])
	stream_shape = np.full((stream_time.shape), y[counter])
	if row["Status"] == 'AVAILABLE':
		plt.plot(stream_time, stream_shape, linewidth=10, color='blue')
	elif row["Status"] == 'NOT_AVAILABLE':
		plt.plot(stream_time, stream_shape, linewidth=10, color='blue')
	elif row["Status"] == 'NOT_EVALUATED':
		plt.plot(stream_time, stream_shape, linewidth=10, color='blue')
	elif row["Status"] == 'PENDING_INGEST':
		plt.plot(stream_time, stream_shape, linewidth=10, color='blue')
counter = counter -1



# plot subsite timelines
for index, row in stream_df.iterrows():
	stream_time = np.array([row["StartTime"],row["EndTime"]])
	stream_shape = np.full((stream_time.shape), y[counter])
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

for index, row in assets_df.iterrows():
	node_time = np.array([row["StartTime"],row["EndTime"]])
	node_shape = np.full((node_time.shape), y[counter])
	if len(row["Level"]) == 14 and type(row["Status"]) == str and row["Level"] == node_name:
		plt.plot(node_time, node_shape, linewidth=10, color='gray',zorder = 3)
counter = counter -1



# plot instrument timelines
for index, row in stream_df.iterrows():
	stream_time = np.array([row["StartTime"],row["EndTime"]])
	stream_shape = np.full((stream_time.shape), y[counter])
	if row["Status"] == 'AVAILABLE':
		plt.plot(stream_time, stream_shape, linewidth=10, color='green')
	elif row["Status"] == 'NOT_AVAILABLE':
		plt.plot(stream_time, stream_shape, linewidth=10, color='green')
	elif row["Status"] == 'NOT_EVALUATED':
		plt.plot(stream_time, stream_shape, linewidth=10, color='green')
	elif row["Status"] == 'PENDING_INGEST':
		plt.plot(stream_time, stream_shape, linewidth=10, color='green')

for index, row in assets_df.iterrows():
	subsite_time = np.array([row["StartTime"],row["EndTime"]])
	subsite_shape = np.full((subsite_time.shape), y[counter])
	if len(row["Level"]) == 8 and type(row["Status"]) == str:
		plt.plot(subsite_time, subsite_shape, linewidth=10, color='gray',zorder = 4)

for index, row in assets_df.iterrows():
	node_time = np.array([row["StartTime"],row["EndTime"]])
	node_shape = np.full((node_time.shape), y[counter])
	if len(row["Level"]) == 14 and type(row["Status"]) == str and row["Level"] == node_name:
		plt.plot(node_time, node_shape, linewidth=10, color='gray',zorder = 4)

for index, row in assets_df.iterrows():
	instrument_time = np.array([row["StartTime"],row["EndTime"]])
	instrument_shape = np.full((instrument_time.shape), y[counter])
	if len(row["Level"]) == 27 and type(row["Status"]) == str and row["Level"]==reference_designator:
		plt.plot(instrument_time, instrument_shape, linewidth=10, color='gray',zorder = 4)
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
