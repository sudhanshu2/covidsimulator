import os
import pandas as pd
import numpy as np

_PATH = "data/"


print("Setting up data directories ...\n")

os.mkdir("data")


link = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
df = pd.read_csv(link)
countries = df["Country/Region"].unique()


for c in countries:
    try:
        os.mkdir(_PATH + str(c))
    except FileExistsError:
        continue

print("Done\n")
