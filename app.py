from flask import Flask, render_template
import plotly
import plotly.express as px


app = Flask(__name__)

@app.route('/')
def index():
    return ('hello world')


# New route for heatmaps

@app.route('/saint_heatmaps')

def saint_heatmaps():
    import plotly.io as pio
    import pandas as pd
    import os
    from geopy.geocoders import Nominatim
    from geopy.extra.rate_limiter import RateLimiter

    cache_file = 'saintbirthlocationmap_geocoded.csv'
    if os.path.exists(cache_file):
        df = pd.read_csv(cache_file)
    else:
        df = pd.read_csv('saintbirthlocationmap.csv')
        geolocator = Nominatim(user_agent="saint_geocoder")
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

        def build_location(row, prefix):
            parts = [row.get(f"{prefix} Location: Specific", ""), row.get(f"{prefix} Region", ""), row.get(f"{prefix} Country", "")]
            return ', '.join([str(p).strip() for p in parts if pd.notnull(p) and str(p).strip().lower() != 'null' and str(p).strip() != ''])

        df['Birth Location Query'] = df.apply(lambda row: build_location(row, 'Birth'), axis=1)
        df['Death Location Query'] = df.apply(lambda row: build_location(row, 'Death'), axis=1)

        df['Birth Latitude'] = None
        df['Birth Longitude'] = None
        df['Death Latitude'] = None
        df['Death Longitude'] = None

        for idx, row in df.iterrows():
            # Birth location
            loc = row['Birth Location Query']
            if loc:
                location = geocode(loc)
                if location:
                    df.at[idx, 'Birth Latitude'] = location.latitude
                    df.at[idx, 'Birth Longitude'] = location.longitude
            # Death location
            loc = row['Death Location Query']
            if loc:
                location = geocode(loc)
                if location:
                    df.at[idx, 'Death Latitude'] = location.latitude
                    df.at[idx, 'Death Longitude'] = location.longitude

        df.to_csv(cache_file, index=False)

    # Drop rows without coordinates
    birth_df = df.dropna(subset=['Birth Latitude', 'Birth Longitude'])
    death_df = df.dropna(subset=['Death Latitude', 'Death Longitude'])

    fig_birth = px.density_mapbox(
        birth_df,
        lat='Birth Latitude',
        lon='Birth Longitude',
        radius=10,
        center=dict(lat=55, lon=-3),
        zoom=4,
        mapbox_style='open-street-map',
        title='Saints Birth Locations Density Map'
    )

    fig_death = px.density_mapbox(
        death_df,
        lat='Death Latitude',
        lon='Death Longitude',
        radius=10,
        center=dict(lat=55, lon=-3),
        zoom=4,
        mapbox_style='open-street-map',
        title='Saints Death Locations Density Map'
    )

    birth_html = pio.to_html(fig_birth, full_html=False)
    death_html = pio.to_html(fig_death, full_html=False)
    return render_template('saint_heatmaps.html', birth_html=birth_html, death_html=death_html)

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