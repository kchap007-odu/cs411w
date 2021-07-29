import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


read = pd.read_json('data_chart.json')

current_fridge_temperature_mean = np.mean(read['Current Fridge Temperature'])
target_fridge_temperature_mean = np.mean(read['Target Fridge Temperature'])
current_freezer_temperature_mean = np.mean(read['Current Freezer Temperature'])
target_freezer_temperature_mean = np.mean(read['Target Freezer Temperature'])
energy_use_mean = np.mean(read['Energy Use'])

xAxis = ['Current Fridge Temperature', 'Target Fridge Temperature',
         'Current Freezer Temperature', 'Target Freezer Temperature']
yAxis = [current_fridge_temperature_mean, target_fridge_temperature_mean,
         current_freezer_temperature_mean, target_freezer_temperature_mean]

plt.bar(xAxis, yAxis)
plt.title('Mean')
plt.xticks(rotation=45)
plt.show()
