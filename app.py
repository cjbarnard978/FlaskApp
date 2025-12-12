from flask import Flask, render_template
import plotly.graph_objects as go
import os
import pandas as pd

app = Flask(__name__)
@app.route('/home')
def home():
    return render_template('home.html')

# Combined saints visualizations route
@app.route('/thesaints')
def saints_combined():
    import pandas as pd
    import plotly.graph_objects as go
    import plotly.express as px
    df = pd.read_csv('SaintBirths.csv')
    # Saint lines map with birth/death markers
    fig = go.Figure()
    # Add legend entries for birth and death markers
    # Add a single birth and death marker for legend
    fig.add_trace(go.Scattermapbox(
        mode = "markers",
        lon = [None],
        lat = [None],
        marker = dict(size=10, color='red'),
        name = "Birth (red)",
        showlegend=True,
        hoverinfo='skip'
    ))
    fig.add_trace(go.Scattermapbox(
        mode = "markers",
        lon = [None],
        lat = [None],
        marker = dict(size=10, color='black'),
        name = "Death (black)",
        showlegend=True,
        hoverinfo='skip'
    ))

    # Use relative path for interactivemonasterymap.csv
    # monastery_df = pd.read_csv('interactivemonasterymap.csv')
    for _, row in df.iterrows():
        if pd.notna(row['Birth_Latitude']) and pd.notna(row['Death_Latitude']) and pd.notna(row['Birth_ Longitude']) and pd.notna(row['Death_Longitude']):
            # Line connecting birth and death
            fig.add_trace(go.Scattermapbox(
                mode = "lines",
                lon = [float(row['Birth_ Longitude']), float(row['Death_Longitude'])],
                lat = [float(row['Birth_Latitude']), float(row['Death_Latitude'])],
                line = dict(width=2, color='blue'),
                name = row['Saint'],
                showlegend=True,
                hoverinfo='text',
                text=f"{row['Saint']}"
            ))
            # Birth marker (red), legend hidden
            fig.add_trace(go.Scattermapbox(
                mode = "markers",
                lon = [float(row['Birth_ Longitude'])],
                lat = [float(row['Birth_Latitude'])],
                marker = dict(size=10, color='red'),
                name = f"Birth: {row['Saint']}",
                showlegend=False,
                hoverinfo='text',
                text=f"Birth: {row['Saint']}"
            ))
            # Death marker (black), legend hidden
            fig.add_trace(go.Scattermapbox(
                mode = "markers",
                lon = [float(row['Death_Longitude'])],
                lat = [float(row['Death_Latitude'])],
                marker = dict(size=10, color='black'),
                name = f"Death: {row['Saint']}",
                showlegend=False,
                hoverinfo='text',
                text=f"Death: {row['Saint']}"
            ))
    fig.update_layout(
        mapbox = dict(
            style = "open-street-map",
            center = dict(lat=54, lon=-3),
            zoom = 3
        ),
        showlegend = True,
        title = ''
    )
    saint_lines_html = fig.to_html(full_html=False)
    # Bar charts
    birth_counts = df['Birth-Region'].value_counts().reset_index()
    birth_counts.columns = ['Birth-Region', 'Count']
    births_fig = px.bar(birth_counts, x='Birth-Region', y='Count', title='Saint Births by Region', text='Count')
    births_fig.update_traces(textposition='outside')
    births_fig.update_yaxes(range=[0, 5])
    death_counts = df['Death_Region'].value_counts().reset_index()
    death_counts.columns = ['Death_Region', 'Count']
    deaths_fig = px.bar(death_counts, x='Death_Region', y='Count', title='Saint Deaths by Region', text='Count')
    deaths_fig.update_traces(textposition='outside')
    deaths_fig.update_yaxes(range=[0, 6])
    births_bar_html = births_fig.to_html(full_html=False)
    deaths_bar_html = deaths_fig.to_html(full_html=False)
    return render_template('saints_combined.html', saint_lines_html=saint_lines_html, births_pie_html=births_bar_html, deaths_pie_html=deaths_bar_html)

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
            color='red',
            opacity=0.7
        ),
        text=hover_text,
        hoverinfo='text'
    ))
    fig.update_layout(
        title='',
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
            zoom=6,
            style='open-street-map'
        ),
    )
    monastery_html = fig.to_html(full_html=False)
    return render_template('monasteries.html', monastery_html=monastery_html)

if __name__ == '__main__':
    app.run(debug=True, port=5001)