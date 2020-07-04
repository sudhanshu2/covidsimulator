''' references =
https://github.com/baurls/Covid-19-Visualization
https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset?select=covid_19_data.csv
'''
import io
import csv
import pandas as pd
import os
import numpy as np
from plotly import *
import matplotlib
import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, save
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import annotations, Legend, LegendItem, DatetimeTickFormatter
from bokeh.io import export_png
from bokeh.layouts import row

file_path = "direct_data/covid_19_data.csv"

#colums of data in the csv file: covid_19_data.csv
class Columns:
	SNO = 'SNo'
	OBSERVATION_DATE = 'ObservationDate'
	PROVINCE = 'Province/State'
	COUNTRY = 'Country/Region'
	LAST_UPDATE = 'Last Update'
	CONFIRMED = 'Confirmed'
	DEATHS = 'Deaths'
	RECOVERED = 'Recovered'
	ALL = [SNO, OBSERVATION_DATE, PROVINCE, COUNTRY, LAST_UPDATE, CONFIRMED, DEATHS, RECOVERED]

class constants:
	DATA_PATH = 'direct_data/'
	APP_NAME = 'Covid Simulation'

class DataLayer:
	# data parsing class taking from the github repo referenced at the top of the link
	def __init__(self, datafile):
		#load the data given
		#strore it in a more specific data format
		#anser querys from VierController
		self.__process_input_data(datafile)

	# private utility methods
	def __process_input_data(self, datafile):
		global parsed_data_frame # this stores the global variables
		dframe=pd.read_csv(datafile)
		self.dataframe = dframe

		#get all countries
		countries = dframe[Columns.COUNTRY].unique()
		self.all_countries = countries


		#add all provinces to country
		self.province_mapping = {}
		for country in self.all_countries:
			country_indices = dframe[Columns.COUNTRY] == country
			provinces = dframe[country_indices][Columns.PROVINCE].unique()
			self.province_mapping[country] = list(provinces)

		#get all dates available
		self.total_days_recorded = dframe[Columns.OBSERVATION_DATE].unique()
		self.accum_deaths_for_day = {}
		self.accum_recovery_for_day = {}
		self.accum_confirms_for_day = {}

		for day in self.total_days_recorded:
			current_day_indices = dframe[Columns.OBSERVATION_DATE] == day
			total_day_deaths = dframe[current_day_indices][Columns.DEATHS].sum()
			total_day_recovers = dframe[current_day_indices][Columns.RECOVERED].sum()
			total_day_confirmed = dframe[current_day_indices][Columns.CONFIRMED].sum()

			self.accum_deaths_for_day[day] = total_day_deaths
			self.accum_recovery_for_day[day] = total_day_recovers
			self.accum_confirms_for_day[day] = total_day_confirmed


		parsed_data_frame = dframe
		self.geo_map_dataframe = self.dataframe.rename(columns={'Country/Region':'Country'}) #copy & rename
		self.geo_map_dataframe.rename(columns={'ObservationDate':'Date'}, inplace=True) #only rename


	# these are public
	def get_map_dataframe(self):
		final_df = self.geo_map_dataframe[self.geo_map_dataframe['Confirmed']>0]
		return final_df.groupby(['Date','Country']).sum().reset_index()

	def get_as_of_date(self):
		no_days = len(self.total_days_recorded)
		return self.total_days_recorded[no_days - 1]

	def get_all_days_recorded(self):
		return self.total_days_recorded

	def get_all_countries(self):
		return self.all_countries



def get_country_data(df, country):
	u_df = df.loc[df['Country'] == country]
	cases = {}
	deaths = {}
	recovered = {}
	for i, j in u_df.iterrows():
		date = j['Date']
		if date in cases:
			cases[date] += j['Confirmed']
			deaths[date] += j['Deaths']
			recovered[date] += j['Recovered']
		else:
			cases[date] = j['Confirmed']
			deaths[date] = j['Deaths']
			recovered[date] = j['Recovered']

	c_data = [value for key,value in cases.items()]
	d_data = [value for key,value in deaths.items()]
	r_data = [value for key,value in recovered.items()]


	return [c_data, d_data, r_data]

def plot():
	'''
	function to use either pyplot or bokeh to plot the global data frame variable
	that contains all the updated data
	'''
	process = DataLayer(file_path)
	countries = list(process.get_all_countries())
	init_dframe = process.get_map_dataframe()
	dframe = [get_country_data(init_dframe, countries[i]) for i in range(len(countries))]
	all_dates = list(process.total_days_recorded)
	current = 0
	counter = []
	for date in all_dates:
		current = current + 1
		counter.append(current)

	# this bokeh style graphing is in the same format that sudhanshu used in the colab
	# for the initial plots with state data in India
	line_colors = ["#4CAF50", "#F44336"]

	#p_list = []

	for i in range(len(countries)):
		'''
		plt.plot(dframe[i][0])
		plt.plot(dframe[i][1])
		plt.plot(dframe[i][2])
		plt.tick_params(
		axis='x',          # changes apply to the x-axis
		which='both',      # both major and minor ticks are affected
		bottom=False,      # ticks along the bottom edge are off
		top=False,         # ticks along the top edge are off
		labelbottom=False)
		country_string = str(countries[i])
		plt.title(country_string)
		plt.savefig(country_string+'.png', dpi=300, bbox_inches='tight')
		plt.close()
		'''
		# xs = [all_dates, all_dates]
		xs = [counter, counter]
		ys = [dframe[i][0], dframe[i][1]]
		per_day = figure(plot_width=900, plot_height=500)
		r_per_day = per_day.multi_line(xs, ys, color=line_colors, line_alpha=0.6, line_width=5)
		legend_per_day = Legend(items=[
			LegendItem(label="cases per day", renderers=[r_per_day], index=0),
			LegendItem(label="death per day", renderers=[r_per_day], index=1),
		])
		per_day.add_layout(legend_per_day)
		# p_list.append(per_day)
		export_png(per_day, filename = "plots/"+str(countries[i])+".png")
	# show(row(p_list))
	return None

def main():
	plot()

if __name__ == '__main__':
	main()
