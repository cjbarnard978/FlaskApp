
from flask import Flask, render_template
import plotly.express as px

app = Flask(__name__)

# Route to display choropleth maps for births and deaths using the combined province GeoJSON
@app.route('/saintsbirthsanddeaths')
def saints_choropleth_maps():
    import plotly.io as pio
    import pandas as pd
    import json
    # Load data and combined geojson
    df = pd.read_csv('saintbirthlocationmap.csv')
    with open('Ireland_ADM1_simplified.simplified.geojson', 'gb.json', 'r') as f:
        provinces_geojson = json.load(f)

    # Province maps
    birth_prov_counts = df['Birth Country'].value_counts().reset_index()
    birth_prov_counts.columns = ['region', 'count']
    fig_birth_prov = pio.to_html(
        px.choropleth_mapbox(
            birth_prov_counts,
            geojson=provinces_geojson,
            locations='region',
            color='count',
            featureidkey='properties.shapeName',
            mapbox_style='open-street-map',
            center={'lat': 53.5, 'lon': -7.5},
            zoom=5,
            title='Saints Births'
        ), full_html=False)

    death_prov_counts = df['Death Country'].value_counts().reset_index()
    death_prov_counts.columns = ['region', 'count']
    fig_death_prov = pio.to_html(
        px.choropleth_mapbox(
            death_prov_counts,
            geojson=provinces_geojson,
            locations='region',
            color='count',
            featureidkey='properties.shapeName',
            mapbox_style='open-street-map',
            center={'lat': 53.5, 'lon': -7.5},
            zoom=5,
            title='Saints Deaths'
        ), full_html=False)

    return render_template('saints_choropleth_maps.html',
        birth_prov_html=fig_birth_prov,
        death_prov_html=fig_death_prov)


@app.route('/monasteries')
def monasteries():
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
    monastery_html = go.Figure(fig).to_html(full_html=False)
    return render_template('monasteries.html', monastery_html=monastery_html)

if __name__ == '__main__':
    app.run(debug=True, port=5000)