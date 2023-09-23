# Step 4: Import necessary libraries
import dash
import rasterio as rio
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import geopandas as gpd
import numpy as np

# Step 5: Create a Dash app
app = dash.Dash(__name__)

# Step 6: Load your geospatial data
gdf = gpd.read_file("C:/Users/clayt/Downloads/2011-2020.shp")

with rio.open("C:/Users/clayt/Downloads/2011-2020-idw.tif") as src:
    
    temp = src.read(1)
    print(temp)

# norm = np.linalg.norm(temp)

# norm_arr = temp/norm

# print(temp)

# normalized_matrix = normalize_2d(temp)

# a scientific colorscale for dem data
bamako= [[0.0, 'rgb(0, 63, 76)'], 
 [0, 'rgb(29, 81, 59)'],
 [0.2, 'rgb(55, 98, 43)'],
 [0.3, 'rgb(79, 114, 30)'],
 [0.4, 'rgb(103, 129, 16)'],
 [0.5, 'rgb(136, 142, 2)'],
 [0.6, 'rgb(169, 154, 21)'],
 [0.7, 'rgb(192, 171, 45)'],
 [0.8, 'rgb(214, 188, 74)'],
 [0.9, 'rgb(234, 209, 112)'],
 [1.0, 'rgb(254, 229, 152)']]

# Step 7: Define the layout of your dashboard
app.layout = html.Div([
    html.H1("Geospatial Dashboard", style={"background": "red", "padding": "8px 16px"}),
    
    # Dropdown for selecting a variable to visualize
    dcc.Dropdown(
        id='variable-dropdown',
        options=[
            {'label': column, 'value': column} for column in gdf.columns
        ],
        value=gdf.columns[0],  # Default selection
        multi=False
    ),
    
    # Geospatial map
    dcc.Graph(
        id='geo-map'
    )
])

# Step 8: Create callback function to update the map
@app.callback(
    Output('geo-map', 'figure'),
    Input('variable-dropdown', 'value')
)
def update_map(selected_variable):
    # fig= px.imshow(temp, color_continuous_scale=bamako)
    fig = px.choropleth(
        gdf,
        geojson=gdf.geometry,
        locations=gdf.index,
        color=selected_variable,
        projection="mercator"
    )
    
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        title=f"{selected_variable} Distribution",
        coloraxis_showscale=True
    )
    
    return fig

# Step 9: Run the app
if __name__ == '__main__':
    app.run_server(debug=True)