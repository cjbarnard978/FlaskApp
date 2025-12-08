import json
import pandas as pd
import plotly.express as px

# Load county and province geojson files
with open('gb.json', 'r') as f:
    counties_geojson = json.load(f)
with open('Ireland_ADM1_simplified.simplified.geojson', 'r') as f:
    provinces_geojson = json.load(f)

def plot_choropleth(df, region_col, geojson, featureidkey, title):
    counts = df[region_col].value_counts().reset_index()
    counts.columns = ['region', 'count']
    fig = px.choropleth_mapbox(
        counts,
        geojson=geojson,
        locations='region',
        color='count',
        featureidkey=featureidkey,
        mapbox_style='open-street-map',
        center={'lat': 53.5, 'lon': -7.5},
        zoom=5,
        title=title
    )
    fig.show()

# Load data
saints_df = pd.read_csv('saintbirthlocationmap.csv')

# County choropleth maps
plot_choropleth(saints_df, 'Birth Region', counties_geojson, 'properties.NAME', 'Saints Births by County')
plot_choropleth(saints_df, 'Death Region', counties_geojson, 'properties.NAME', 'Saints Deaths by County')

# Province choropleth maps
plot_choropleth(saints_df, 'Birth Country', provinces_geojson, 'properties.shapeName', 'Saints Births by Province')
plot_choropleth(saints_df, 'Death Country', provinces_geojson, 'properties.shapeName', 'Saints Deaths by Province')
