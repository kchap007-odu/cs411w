import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# function definition that takes Temp_xAxis and Mean_yAxis values as input and plot graph using pyplot

def plot_graph(Temp_xAxis, Mean_yAxis):
    plt.bar(Temp_xAxis, Mean_yAxis)
    plt.title('Mean')
    plt.xticks(rotation=45)
    plt.show()


read = pd.read_json('data_chart.json')

current_fridge_temperature_mean = np.mean(read['Current Fridge Temperature'])
target_fridge_temperature_mean = np.mean(read['Target Fridge Temperature'])
current_freezer_temperature_mean = np.mean(read['Current Freezer Temperature'])
target_freezer_temperature_mean = np.mean(read['Target Freezer Temperature'])
energy_use_mean = np.mean(read['Energy Use'])

Temp_xAxis = ['Current Fridge Temperature', 'Target Fridge Temperature',
         'Current Freezer Temperature', 'Target Freezer Temperature']
Mean_yAxis = [current_fridge_temperature_mean, target_fridge_temperature_mean,
         current_freezer_temperature_mean, target_freezer_temperature_mean]

# calling function to plot the graph with parameters Temp_xAxis and Mean_yAxis

plot_graph(Temp_xAxis, Mean_yAxis)
