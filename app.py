from flask import Flask, render_template
import plotly.graph_objects as go
import pandas as pd

app = Flask(__name__)

@app.route('/saints')
def saints():
    import pandas as pd
    import plotly.graph_objects as go
    saints = pd.read_csv('SaintBirths.csv')
    fig = go.Figure()
    for _, row in saints.iterrows():
        if pd.notna(row['Birth_Latitude']) and pd.notna(row['Death_Latitude']) and pd.notna(row['Birth_ Longitude']) and pd.notna(row['Death_Longitude']):
            fig.add_trace(go.Scattermapbox(
                mode = "lines",
                lon = [float(row['Birth_ Longitude']), float(row['Death_Longitude'])],
                lat = [float(row['Birth_Latitude']), float(row['Death_Latitude'])],
                line = dict(width=2, color='blue'),
                name = row['Saint']
            ))
    fig.update_layout(
        mapbox = dict(
            style = "open-street-map",
            center = dict(lat=54, lon=-3),
            zoom = 4
        ),
        showlegend = True,
        title = "Saints' Birth to Death Locations"
    )
    saint_lines_html = fig.to_html(full_html=False)
    return render_template('saint_lines.html', saint_lines_html=saint_lines_html)

@app.route('/saint_pies')
def saints():
    import plotly.express as px
    df = pd.read_csv('SaintBirths.csv')
    df = px.data.tips()
    fig = px.pie(df, values='Birth_Region', names='Birth_Region', title = 'Saint Births by Region')
    fig.show()
    saint_pie_html = fig.to_html(full_html=False)

    df = pd.read_csv('SaintBirths.csv')
    df = px.data.tips()
    fig = px.pie(df, values='Death_Region', names='Death_Region',title = 'Saint Deaths by Region')
    fig.show()
    saint_death_pie_html = fig.to_html(full_html=False)
    return render_template('saint_pies.html', saint_pie_html=saint_pie_html, saint_death_pie_html=saint_death_pie_html)

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