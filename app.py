
from flask import Flask, render_template
import plotly.graph_objects as go
import pandas as pd

app = Flask(__name__)

@app.route('/birth_region_choropleth')
def birth_region_choropleth():
    import plotly.express as px
    import json
    df = pd.read_csv('SaintBirths_geocoded.csv')
    # Count births per region
    birth_counts = df['Birth Region'].value_counts().reset_index()
    birth_counts.columns = ['region', 'count']
    # Merge coordinates
    coords = df[['Birth Region', 'Birth Region Latitude', 'Birth Region Longitude']].drop_duplicates()
    birth_counts = birth_counts.merge(coords, left_on='region', right_on='Birth Region', how='left')
    # Load the combined GeoJSON file
    with open('geojson/combined_british_isles.geojson', 'r') as f:
        geojson = json.load(f)
    fig = px.choropleth_mapbox(
        birth_counts,
        geojson=geojson,
        locations='region',
        color='count',
        featureidkey='properties.name',
        mapbox_style='open-street-map',
        center={'lat': 53.5, 'lon': -7.5},
        zoom=5,
        title='Saints Births by Region'
    )
    birth_region_choropleth_html = fig.to_html(full_html=False)
    return render_template('birth_region_choropleth.html', birth_region_choropleth_html=birth_region_choropleth_html)



@app.route('/monasteries')
def monasteries():
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
    monastery_html = fig.to_html(full_html=False)
    return render_template('monasteries.html', monastery_html=monastery_html)


if __name__ == '__main__':
    app.run(debug=True, port=5001)