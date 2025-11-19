from flask import Flask, render_template
import plotly
import plotly.express as px

app = Flask(__name__)

@app.route('/')
def index():
    return ('hello world')

@app.route('/visualizations')
def visualizations():
    import pandas as pd
    df = pd.read_csv('saints.csv')
    fig1 = px.line(df, x="Name", y="Death_Date", title='Death Date of Irish and Scottish Saints')
    graph_html1 = fig1.to_html(full_html=False)

    # Second visualization (density map)
    if 'Birth_Location' in df.columns:
        fig2 = px.density_mapbox(df, lat='Birth_Location', lon='Birth_Location', radius=10,
                                center=dict(lat=53.3498, lon=6.2603), zoom=0,
                                mapbox_style="open-street-map")
        graph_html2 = fig2.to_html(full_html=False)
    else:
        graph_html2 = '<p>Density map data not available.</p>'

    if 'Sex' in df.columns:
        fig3 = px.pie(df, names='Sex', title='Sex Distribution of Saints')
        graph_html3 = fig3.to_html(full_html=False)
    else:
        graph_html3 = '<p>Pie chart not available.</p>'
    return render_template('visualization.html', plot_html1=graph_html1, plot_html2=graph_html2, plot_html3=graph_html3)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

