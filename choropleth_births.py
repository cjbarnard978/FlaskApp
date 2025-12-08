import pandas as pd
import plotly.express as px
import json

# Load geocoded data
df = pd.read_csv('saintbirthlocationmap_geocoded.csv')

# Use province if specific location is missing
birth_region = df['Birth Location: Specific'].fillna('').replace('', pd.NA)
birth_region = birth_region.combine_first(df['Birth Region'])
birth_counts = birth_region.value_counts().reset_index()
birth_counts.columns = ['region', 'count']

# Load GeoJSON (should contain regions/counties with 'properties.name')
with open('britishislesgeojson.json', 'r') as f:
    geojson = json.load(f)

# Create choropleth map
fig = px.choropleth_mapbox(
    birth_counts,
    geojson=geojson,
    locations='region',
    color='count',
    featureidkey='properties.name',
    mapbox_style='open-street-map',
    center={'lat': 53.5, 'lon': -7.5},
    zoom=5,
    title='Saints Births by County/Province'
)
fig.show()
