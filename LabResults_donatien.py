# *-* coding: utf-8 *-*

# Read Files
import csv
import pandas as pd

# Mathematic developments
import math as mt
import numpy as np

# Figure and Graphical representation
from matplotlib import pyplot as plt

columns = ['hours', 'minutes', 'seconds',
           'atm pressure', 'atm temperature', 'atm humidity',
           'T108AP', 'T200Gb', 'T201Gb', 'T202Gb', 'T203Gb',
           'T300Wa', 'T304Wa', 'T400Wa', 'T405Wa', 'T406Wa',
           'air flowrate', 'gas flowrate',
           'F303Wa', 'F401Wa', 'P107Ap',
           'CO', 'CO2', 'NO', 'O2', '??']
debits = [20, 24, 28]

"""
We first read the file in which results have been saved and save it into a pandas
DataFrame structure.
"""
#stable_air_time_limits = [57836, 56950, 57340]
stable_air_time_limits = [[0, 1e5],
                          [0, 55509],
                          [0, 55205]]
gas_comp = []
air_flow_rates = []
gas_flow_rate = []
for i in range(len(debits)):
    results = pd.read_csv('results/d'+str(debits[i])+'_donatien.csv')
    results.columns = columns

    results = results[(results['gas flowrate']>0.) & (results['gas flowrate']<5.)]
    results.index = range(len(results))

    time = results['hours']*3600 + results['minutes']*60 + results['seconds']

    stable_air = results['air flowrate'][(time>stable_air_time_limits[i][0]) & (time<stable_air_time_limits[i][1])]
    air_flow_rates.append(np.mean(stable_air))
    gas_flow_rate.extend(list(results['gas flowrate']))

    gc = {}
    for g in ['CO', 'CO2', 'NO', 'O2']:
        gc[g] = results[g][100]
    gas_comp.append(gc)

    plt.figure()
    #plt.plot(stable_air)
    plt.plot(time,results['T201Gb'])
    plt.plot(time,results['T202Gb'])
    plt.plot(time,results['T203Gb'])

T_room = results['atm temperature'][0]+273.15

gas_flow_rate = np.mean(gas_flow_rate)
#print(gas_flow_rate)
#print(air_flow_rates)

if __name__=="__main__":
  plt.show()
  print(gas_comp)
