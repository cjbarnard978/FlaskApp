About the App

This app is an in-progress data visualization repository for "Mission, Myth, and Monasticism: Religious Archetypes and Cultural Transmission between Gaelic Ireland and Scotland, 1200-1500," a project I will be presenting at ICMS 2026 in May. This flask app uses plotly.js and Bootstrap to create spatial visualizations and bar charts to explore the cultural spread of Christianity from Ireland to Scotland in the early medieval period. In future, the app will also contain visualizations for topic modeling and word embedding to discuss the maintenance of that cultural communication in the High and Late Middle Ages. 

The Visualizations 

"Seven 12th Century Scottish Monasteries:"
    Code Documentation Link: https://plotly.com/python/tile-scatter-maps/ 
    This is an interactive scatter map built using plotly express and geopandas. The code allows for the linkage of Google Street View to the points. When clicked, the code opens a new tab in Google Street View using the coordinates in "interactivemonasterymap.csv." 

Bar Charts:
    Code Documentation Link:https://plotly.com/python/bar-charts/ 
    These bar charts are a statistical representation of the data in "The Migration of Early Saints." They're built using plotly express and pandas. Since the line map does not represent the spread of birth and death locations in an accessible way, these bar charts were added for ease of understanding and clarity.

"The Migration of Early Saints:" 
    Code Documentation Link: https://plotly.com/python/lines-on-maps/ 
    This interactive line map was built using plotly express and pandas. It allows saints to be deselected to avoid cluttering the visualization. The dots are color coded: red is birth place, black is death location. The goal of this visualization is to demonstrate the mobility or lack thereof of early medieval saints important in Scotland and Ireland. The text box to the left of the visualization points specifically to a nuanced argument of spatiality and gender differences. 

Installing Flask and Viewing the App 

Installing Flask: pip install Flask 
To run the app: python app.py 
Access the app at: http://localhost:5001/home 
To install the packages required to edit: pip install -r requirements.txt

Setting up and Running the Virtual Environment

Setting up the virtual environment: python -m venv flaskapp_env
Activating flaskapp_env: source flaskapp_env/bin/activate 

Files 

app.py: Contains the python code to run all 4 visualizations housed in the app. 

static folder: contains the background image on the homepage and the .txt files for the text boxes throughout the site.

templates folder:
    base.html: contains the html code to control the navbar, background colors, fonts, and code to allow for it to be extended throughout the site. Navbar and background colors were selected to correspond with the background image on home.html, which is a 16th century map of Scotland from the National Library of Scotland. Citation included in the Flask App Explainer. 
    home.html: contains the html code for the homepage, including the code to integrate the background image. base.html is extended on this template. 
    monasteries.html: contains the html code for the scatter map. Extends base.html
    saints_combined.html: contains the html code for the line map and both bar charts. base.html is extended on this template.

SaintBirths.csv: Raw data for the line map and both bar charts.

interactivemonasterymap.csv: Raw data for the interactive scatter map.

requirements.txt: Required packages and versions used on the Flask app stored here.

readme.md: Contains activation instructions and app documentation. 