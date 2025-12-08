



from flask import Flask, render_template
import plotly.graph_objects as go
import pandas as pd

app = Flask(__name__)

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

# Bubble map for births
@app.route('/births_bubble_map')
def births_bubble_map():
    df = pd.read_csv('saintbirthlocationmap_geocoded.csv')
    # If no specific location, use province
    df['Birth Location'] = df['Birth Location: Specific'].fillna('').replace('', pd.NA)
    df['Birth Location'] = df['Birth Location'].combine_first(df['Birth Region'])
    # Use province coordinates if specific location is missing
    df['Birth Latitude'] = df['Birth Latitude'].combine_first(df['Birth Region'].map(df.groupby('Birth Region')['Birth Latitude'].transform('mean')))
    df['Birth Longitude'] = df['Birth Longitude'].combine_first(df['Birth Region'].map(df.groupby('Birth Region')['Birth Longitude'].transform('mean')))
    df_valid = df.dropna(subset=['Birth Latitude', 'Birth Longitude'])
    birth_counts = df_valid.groupby(['Birth Latitude', 'Birth Longitude', 'Birth Location']).size().reset_index(name='count')
    fig = go.Figure(go.Scattermapbox(
        lat=birth_counts['Birth Latitude'],
        lon=birth_counts['Birth Longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=birth_counts['count']*8,
            color=birth_counts['count'],
            colorscale='Viridis',
            showscale=True,
            sizemode='area',
            opacity=0.7
        ),
        text=birth_counts['Birth Location'] + '<br>Count: ' + birth_counts['count'].astype(str),
        hoverinfo='text'
    ))
    fig.update_layout(
        mapbox=dict(
            style='open-street-map',
            center=dict(lat=53.5, lon=-7.5),
            zoom=5
        ),
        title='Saints Births Bubble Map',
        margin=dict(l=0, r=0, t=40, b=0)
    )
    birth_html = fig.to_html(full_html=False)
    return render_template('births_bubble_map.html', birth_html=birth_html)

# Bubble map for deaths
@app.route('/deaths_bubble_map')
def deaths_bubble_map():
    df = pd.read_csv('saintbirthlocationmap_geocoded.csv')
    # If no specific location, use province
    df['Death Location'] = df['Death Location: Specific'].fillna('').replace('', pd.NA)
    df['Death Location'] = df['Death Location'].combine_first(df['Death Region'])
    # Use province coordinates if specific location is missing
    df['Death Latitude'] = df['Death Latitude'].combine_first(df['Death Region'].map(df.groupby('Death Region')['Death Latitude'].transform('mean')))
    df['Death Longitude'] = df['Death Longitude'].combine_first(df['Death Region'].map(df.groupby('Death Region')['Death Longitude'].transform('mean')))
    df_valid = df.dropna(subset=['Death Latitude', 'Death Longitude'])
    death_counts = df_valid.groupby(['Death Latitude', 'Death Longitude', 'Death Location']).size().reset_index(name='count')
    fig = go.Figure(go.Scattermapbox(
        lat=death_counts['Death Latitude'],
        lon=death_counts['Death Longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=death_counts['count']*8,
            color=death_counts['count'],
            colorscale='Viridis',
            showscale=True,
            sizemode='area',
            opacity=0.7
        ),
        text=death_counts['Death Location'] + '<br>Count: ' + death_counts['count'].astype(str),
        hoverinfo='text'
    ))
    fig.update_layout(
        mapbox=dict(
            style='open-street-map',
            center=dict(lat=53.5, lon=-7.5),
            zoom=5
        ),
        title='Saints Deaths Bubble Map',
        margin=dict(l=0, r=0, t=40, b=0)
    )
    death_html = fig.to_html(full_html=False)
    return render_template('deaths_bubble_map.html', death_html=death_html)

if __name__ == '__main__':
    app.run(debug=True, port=5001)