from flask import Flask, render_template
import plotly
import plotly.express as px

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visualizations')
def visualizations():
    import pandas as pd
    df = pd.read_csv("saints.csv")
    fig = px.line(df, x="Name", y="Death_date", title='Death Date of Irish and Scottish Saints')
    graph_html = fig.to_html(full_html=False)
    return render_template('visualization.html', plot_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

