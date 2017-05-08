#!/usr/bin/env python
"""
@Author: Leila Belabbassi
@Date: May 01, 2017
@Goal: get the start and end dates of a time range to annotate a specific event in the data
"""

import netCDF4 as nc
import numpy as np


file = '/Users/leila/Downloads/deployment0002_CE04OSPS-SF01B-2A-CTDPFA107-streamed-ctdpf_sbe43_sample_20151201T120000.033304-20151223T115959.802833.nc'


# read data file and varaibles
#
f = nc.Dataset(file)
t = f.variables['time']
units = t.units
dates = nc.num2date(t[:], units=units)
x = f.variables['seawater_pressure']


# select data based on a condition, e.g. 150 umol L-1
value_x = np.array(x[:])
time_x = np.array(t[:])
ii = np.where(value_x > 6000)

# get the start date of the conditional data
index_1 = ii[0][0]
value_1 = value_x[index_1]
time_1 = dates[index_1]
time_1 = time_1.strftime('%Y-%m-%dT%H:%M:%SZ')
print value_1, '   ', time_1

# get the end date of the conditional data
index_n = ii[0][len(ii[0])-1]
value_n = value_x[index_n]
time_n = dates[index_n]
time_n = time_n.strftime('%Y-%m-%dT%H:%M:%SZ')
print value_n, '   ', time_n