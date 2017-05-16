#!/usr/bin/env python
"""
@Author: Leila Belabbassi
@Date:  May 03, 2017
@Goal: investigate a time range to verify an annotation
"""

import datetime
import netCDF4 as nc
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np


nc_file = '/Users/leila/Downloads/deployment0004_CP02PMUO-WFP01-03-CTDPFK000-recovered_wfp-ctdpf_ckl_wfp_instrument_recovered_20141005T220003-20150212T211238.987984.nc'

deployment_num = 'deployment[4]'
time_variable = 'time'
param_variable = 'ctdpf_ckl_seawater_pressure'

date_0 = datetime.datetime(2014, 11, 13, 0, 0, 0)
date_n = datetime.datetime(2014, 11, 27, 0, 0, 0)


f = nc.Dataset(nc_file)
y_parameter = f.variables[param_variable]
t_parameter = f.variables[time_variable]
units = t_parameter.units
dates = nc.num2date(t_parameter[:], units=units)
print deployment_num, ': ', dates[0], ' - ', dates[-1]

time_x = np.array(dates[:])
ind = np.intersect1d(np.where(dates > date_0), np.where(dates < date_n))

time_xx = time_x[ind]
print time_xx

parameter_yy = y_parameter[ind]
print parameter_yy

ylim_min = min(parameter_yy)
ylim_max = max(parameter_yy)

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%dT%H:%M:%SZ'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())

plt.plot(time_xx, parameter_yy, 'ko', markerfacecolor='white', markersize=8)
plt.gcf().autofmt_xdate()
plt.ylim([ylim_min,ylim_max])
plt.xlabel('Time UTC')
plt.ylabel(param_variable)
plt.draw()
# #
plt.show()
# time.sleep(0.05)