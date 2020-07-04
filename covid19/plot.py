import requests
import os
import ijson
import datetime

from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.models import annotations, Legend, LegendItem, DatetimeTickFormatter
from bokeh.layouts import row

from bokeh.plotting import figure, output_file, show

url = "https://opendata.ecdc.europa.eu/covid19/casedistribution/json"
file_name = "data.json"

with requests.get(url, stream=True) as r:
  r.raise_for_status()
  with open(file_name, "wb") as f:
    chunk_count = 0
    for chunk in r.iter_content(chunk_size=512):
      chunk_count += 1
      f.write(chunk)

print("retrieved the file of size " + str(os.stat(file_name).st_size / 1000000) + " MB in " + str(chunk_count) + " chunks")

cases_per_day = []
death_per_day = []
dates = []

counter = []
cases = []
death = []

date_current = datetime.date.today()
case_count = 0
death_count = 0
current = 0

with open("data.json", 'r') as covid_data:
  parser = ijson.parse(covid_data)
  for prefix, event, value in parser:
    if prefix == "records.item.dateRep":
      date_current = datetime.datetime.strptime(value, "%d/%m/%Y").date()
    if prefix == "records.item.cases":
      case_count = int(value)
    if prefix == "records.item.deaths":
      death_count = int(value)
    if prefix == "records.item.countriesAndTerritories" and value == "India":
      cases_per_day.append(case_count)
      death_per_day.append(death_count)
      dates.append(date_current)
      current = current + 1
      counter.append(current)

cases_per_day.reverse()
death_per_day.reverse()
dates.reverse()

cases.append(cases_per_day[0])
death.append(death_per_day[0])

for i in range(1, len(cases_per_day)):
  cases.append(cases_per_day[i] + cases[i - 1])
  death.append(death_per_day[i] + death[i - 1])

print("done parsing data\n")

date_strings = []

for date in dates:
  date_strings = date.strftime('%d/%m/%Y')

output_file("line.html")

xs = [counter, counter]
ys_per_day = [cases_per_day, death_per_day]
ys_total = [cases, death]

line_colors_per_day = ["#4CAF50", "#F44336"]
line_colors_total = ["#FF9800", "#03A9F4"]

p_per_day = figure(plot_width=800, plot_height=500)
r_per_day = p_per_day.multi_line(xs, ys_per_day, color=line_colors_per_day, line_alpha=0.6, line_width=2)

p_total = figure(plot_width=800, plot_height=500)
r_total = p_total.multi_line(xs, ys_total, color=line_colors_total, line_alpha=0.6, line_width=2)

legend_per_day = Legend(items=[
    LegendItem(label="cases per day", renderers=[r_per_day], index=0),
    LegendItem(label="death per day", renderers=[r_per_day], index=1),
])

legend_total = Legend(items=[
    LegendItem(label="total cases", renderers=[r_total], index=0),
    LegendItem(label="total death", renderers=[r_total], index=1),
])

p_per_day.add_layout(legend_per_day)
p_total.add_layout(legend_total)

# put all the plots in a VBox
p = row(p_per_day, p_total)

# show the results
show(p)
