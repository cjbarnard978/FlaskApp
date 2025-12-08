from flask import Flask, render_template
import plotly.express as px

app = Flask(__name__)

# New route for county and province choropleth maps
@app.route('/saint_choropleths')
def saint_choropleths():
    import plotly.io as pio
    import pandas as pd
    import json
    df = pd.read_csv('saintbirthlocationmap.csv')
    with open('gb.json', 'r') as f:
        counties_geojson = json.load(f)
    with open('Province_Boundaries_Generalised_50m_-4507604732527992184.geojson', 'r') as f:
        provinces_geojson = json.load(f)

    # County choropleth
    birth_counts = df['Birth Region'].value_counts().reset_index()
    birth_counts.columns = ['county', 'count']
    fig_county = pio.to_html(px.choropleth_mapbox(
        birth_counts,
        geojson=counties_geojson,
        locations='county',
        color='count',
        featureidkey='properties.NAME',
        mapbox_style='open-street-map',
        center={'lat': 55, 'lon': -3},
        zoom=4,
        title='Saints Births by County'
    ), full_html=False)

    # Province choropleth
    birth_prov_counts = df['Birth Country'].value_counts().reset_index()
    birth_prov_counts.columns = ['province', 'count']
    fig_province = pio.to_html(px.choropleth_mapbox(
        birth_prov_counts,
        geojson=provinces_geojson,
        locations='province',
        color='count',
        featureidkey='properties.NAME',
        mapbox_style='open-street-map',
        center={'lat': 55, 'lon': -3},
        zoom=4,
        title='Saints Births by Province'
    ), full_html=False)

    return render_template('saint_choropleths.html', county_html=fig_county, province_html=fig_province)
from flask import Flask, render_template

import plotly.graph_objects as go
import pandas as pd
df = pd.read_csv('interactivemonasterymap.csv')
Latitude = df['Latitude']
Longitude = df['Longitude']
monastery_info = df[['Monastery', 'Monastery Type', 'Date founded', 'Founder', 'Current Status']]
hover_text = monastery_info.apply(lambda row: f"Monastery: {row['Monastery']}<br>Type: {row['Monastery Type']}<br>Date Founded: {row['Date founded']}<br>Founder: {row['Founder']}<br>Status: {row['Current Status']}", axis=1)
fig = go.Figure()
fig.add_trace(go.Scattermapbox(
    lat=Latitude,
    lon=Longitude,
    mode='markers',
    marker=dict(
        size=17,
        color='blue',
        opacity=0.7
    ),
    text=hover_text,
    hoverinfo='text'
))
fig.update_layout(
    title='Medieval Monasteries of the Bannatyne Club',
    autosize=True,
    hovermode='closest',
    showlegend=False,
    mapbox=dict(
        bearing=0,
        center=dict(
            lat=55.9523,
            lon=-3.1882
        ),
        pitch=0,
        zoom=5,
        style='open-street-map'
    ),
)

if __name__ == '__main__':
    app.run(debug=True)