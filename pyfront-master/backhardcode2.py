import urllib.request
import json
import json
import autopep8
import sys
import os
import numpy as np
# import pycountry as pc
import pandas as pd
import ipywidgets as widgets
from IPython.display import display
import csv
import itertools
import plotly.plotly as py

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go

init_notebook_mode(connected=True)






# EXTRACTING DATA AND CONVERTING IT TO A 1-DIMENSIONAL ARRAY


def extract():
    with urllib.request.urlopen("http://api.population.io:80/1.0/countries") as url:
        slash = "/"
        api_data = json.loads(url.read().decode())
        # turns the dictionary into a 2D array
        twoD_data = np.array(list(api_data.values()))
        all_countries = twoD_data.ravel()
        return all_countries
        country_code_data = pd.read_csv('https://pkgstore.datahub.io/core/country-list/data_csv/data/d7c9d7cfb42cb69f4422dec222dbbaa8/data_csv.csv')
        df1 = country_code_data[['Name', 'Code']]
        df2 = country_code_data[['Code']]
        test = pd.read_csv("http://kejser.org/wp-content/uploads/2014/06/Country.csv", delimiter='|')
        df3 = test[["CountryName", "Alpha3Code"]]
        country_and_countrycodes = df3.values
        countrycodesTwoD = df2.values
        countrycodes = countrycodesTwoD.ravel()
        chained_country_list = set(itertools.chain.from_iterable(country_and_countrycodes)) & set(all_countries)
        country_ready_for_fetch = []
        for country in chained_country_list:
            try:
                if '/' not in country:
                    j = country.replace(" ", "%20")
                    country_ready_for_fetch.append(j)
            except AttributeError:
                pass
            return chained_country_list


# EXTRACTING THE POPULATION DATA


def populat(country_ready_for_fetch, country_and_countrycodes):
    year = "/2013"
    date = year + '-01-01'
    country_population = []
    for country in country_ready_for_fetch:
        url = "http://api.population.io:80/1.0/population/"

        with urllib.request.urlopen(url + country + date) as url:
            data = json.loads(url.read().decode())
            country_population.append(country)
            country_population.append(data)
            result = {}
            for i in range(0, len(country_population), 2):
                result[country_population[i]] = country_population[i + 1]['total_population']['population']
                result = {key.replace('%20', ' '): value for key, value in result.items()}
                return result


def ending(result, country_and_countrycodes):
    l = np.array(country_and_countrycodes).tolist()
    for i in l:
        i.append(result.get(i[0]))
        df = pd.DataFrame(l)
        df.columns = ['Country', 'CountryCode', 'Population']
        df['CountryCode'] = df['CountryCode'].str.upper()
        data = dict(type='choropleth',
                    locations=df['CountryCode'],
                    z=df['Population'],
                    text=df['Country'],
                    colorscale='Portland',
                    colorbar=dict(title='Population in thousands'))
        layout = dict(title='2013 global Population',
                      geo=dict(showframe=False,
                               showlakes=True,
                               showrivers=True,
                               showcoastlines=True,
                               coastlinewidth=6,
                               coastlinecolor='rgb(127,255,0)',
                               rivercolor='rgb(85,173,240)',
                               lakecolor='rgb(85,173,240)',
                               projection={'type': 'stereographic'}))
        # projection = {'type': 'Mercator'}))
        choromap3 = go.Figure(data=[data], layout=layout)
        plot(choromap3)
        exit = plot(choromap3)
        return exit


