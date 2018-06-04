import os
import folium
import json
import pandas as pd

geo_data = os.path.join('world-countries.json')
geo_json_data = json.load(open(geo_data))

state_data = pd.read_csv('population_data.csv')
m = folium.Map(location=[48, -102], zoom_start=3)
m.choropleth(
    geo_data=geo_data,
    data=state_data,
    columns=['CountryCode', 'Population'],
    threshold_scale=[10000000,150000000,250000000,500000000,2000000000],
    key_on='feature.id',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Unemployment Rate (%)',
    highlight=True
)

m.save(os.path.join('population-map-with-highlighting.html'))


