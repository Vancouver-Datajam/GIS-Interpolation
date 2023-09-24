# Step 4: Import necessary libraries
import dash
import rasterio as rio
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import geopandas as gpd
import pandas as pd
import numpy as np
import csv
from matplotlib import pyplot as plt

from pykrige.ok import OrdinaryKriging
import pykrige.kriging_tools as kt
from sklearn.model_selection import train_test_split

import shapely.geometry as geometry
import itertools
from shapely.geometry import Polygon
import osmnx as ox


# Step 5: Create a Dash app
app = dash.Dash(__name__)


# Step 7: Define the layout of your dashboard
app.layout = html.Div([
    
    html.H1("Geospatial Dashboard", style={"background": "red", "padding": "8px 16px", "margin": 0}),
    html.Div([ 
      dcc.Dropdown(
          id='time-period-dropdown',
          options=[ 
            {'label': '1961-1990', 'value': '1961-1990'},
            {'label': '1991-2000', 'value': '1991-2000'},
            {'label': '2001-2010', 'value': '2001-2010'},
            {'label': '2011-2020', 'value': '2011-2020'}
          ],
          multi=False,
          value="2011-2020",
          searchable=True,
          style={'flex': 1, 'boxShadow': '0px 4px 4px 0px #c0c0c0'}
      ),
      dcc.Dropdown(
          id='target-variable-dropdown',
          options=[
            # max
            {'label': 'Temp Maximum - Winter', 'value': 'Tmax_wt'},
            {'label': 'Temp Maximum - Spring', 'value': 'Tmax_sp'},
            {'label': 'Temp Maximum - Summer', 'value': 'Tmax_sm'},
            {'label': 'Temp Maximum - Fall', 'value': 'Tmax_at'},

            # mins
            {'label': 'Temp Minimum - Winter', 'value': 'Tmin_wt'},
            {'label': 'Temp Minimum - Spring', 'value': 'Tmin_sp'},
            {'label': 'Temp Minimum - Summer', 'value': 'Tmin_sm'},
            {'label': 'Temp Minimum - Fall', 'value': 'Tmin_at'},
            # average
            {'label': 'Temp Average - Winter', 'value': 'Tave_wt'},
            {'label': 'Temp Average - Spring', 'value': 'Tave_sp'},
            {'label': 'Temp Average - Summer', 'value': 'Tave_sm'},
            {'label': 'Temp Average - Fall', 'value': 'Tave_at'},
            # percip
            {'label': 'Precipitation - Winter', 'value': 'PPT_wt'},
            {'label': 'Precipitation - Spring', 'value': 'PPT_sp'},
            {'label': 'Precipitation - Summer', 'value': 'PPT_sm'},
            {'label': 'Precipitation - Fall', 'value': 'PPT_at'},
          ],
          multi=False,
          value="Tmax_wt",
          searchable=True,
          style={'flex': 1, 'boxShadow': '0px 4px 4px 0px #c0c0c0'}
      ),
      dcc.Dropdown(
          id='variable-dropdown',
          options=[ 
            {'label': 'Exponential', 'value': 'exponential'},
            {'label': 'Spherical', 'value': 'spherical'},
            {'label': 'Linear', 'value': 'linear'},
            # {'label': 'Gaussian', 'value': 'Gaussian'},
            # {'label': 'Power', 'value': 'Power'}
          ],
          multi=False,
          value="exponential",
          searchable=True,
          style={'flex': 1, 'boxShadow': '0px 4px 4px 0px #c0c0c0'}
      ),
    ], style={'display': 'flex', 'gap': 24, 'margin': '24px 0px'}),

    html.Div([
      html.Div([    
        html.Div([    
          # Geospatial map
          html.H3("Temperature", style={'textAlign': 'center', 'margin': '8px 0px', 'background': '#fff'}),
          dcc.Graph(
              id='geo-map',
              style={'flex': 1}
          )
        ], style={'border': '1px solid #eaeaea', 'flex': 1, 'boxShadow': '0px 4px 6px 0px #c0c0c0', 'background': '#fff'}),
        html.Div([    
          # Geospatial map
          html.H3("C02", style={'textAlign': 'center', 'margin': '8px 0px', 'background': '#fff'}),
          dcc.Graph(
              id='geo-map-2',
              style={'flex': 1}
          )
        ], style={'border': '1px solid #eaeaea', 'flex': 1, 'boxShadow': '0px 4px 6px 0px #c0c0c0', 'background': '#fff'})
      ], style={'display': 'flex', 'gap': 24, 'width': '100%'})
    ])


    
], style={'minHeight': '100vh', 'margin': -8, 'padding': 0, 'fontFamily': 'Arial'})


# Step 8: Create callback function to update the map
@app.callback(
    Output('geo-map', 'figure'),
    Output('geo-map-2', 'figure'),
    Input('variable-dropdown', 'value'),
    Input('time-period-dropdown', 'value'),
    Input('target-variable-dropdown', 'value')
    # Input('variogram-model-dropdown', 'value')
)
def update_map(variogram, time_period, target_variable):
    # consider 2011-2020 data first

    url_list = [
    # "https://testground.s3.ap-southeast-1.amazonaws.com/3537ea83-529f-471b-92ef-bef6095bb850/1961-1990.csv",
    # "https://testground.s3.ap-southeast-1.amazonaws.com/3537ea83-529f-471b-92ef-bef6095bb850/1991-2000.csv",
    # "https://testground.s3.ap-southeast-1.amazonaws.com/3537ea83-529f-471b-92ef-bef6095bb850/2001-2010.csv",
    # "https://testground.s3.ap-southeast-1.amazonaws.com/3537ea83-529f-471b-92ef-bef6095bb850/2011-2020.csv"
    ]

    baseurl = "https://testground.s3.ap-southeast-1.amazonaws.com/3537ea83-529f-471b-92ef-bef6095bb850/"

    fullUrl = baseurl + time_period + ".csv"

    url_list.append(fullUrl)

    df_list = (pd.read_csv(file) for file in url_list)

    df = pd.concat(df_list, ignore_index=True)

    X = df[['Latitude', 'Longitude']]  # Features: coordinates
    y = df[target_variable]  # Target variable: temp average during winter

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

    resolution = 0.5  # cell size in meters, smaller cell size = smaller pixel = higher resolution 
    gridx = np.arange(df.Latitude.min(), df.Latitude.max(), resolution)
    gridy = np.arange(df.Longitude.min(), df.Longitude.max(), resolution)

    OK = OrdinaryKriging(
        df['Latitude'],
        df['Longitude'],
        df[target_variable],
        variogram_model=variogram,# "spherical" "linear" "gaussian" "power" "exponential"
        # verbose=True,
        enable_plotting=False
    )

    z, ss = OK.execute("grid", gridx, gridy)

      # kt.write_asc_grid(gridx, gridy, z, filename="output.asc")
      # plt.imshow(z)
      # plt.show()

    xgrid,ygrid = np.meshgrid(gridx,gridy)

    def pixel2poly(x, y, z, resolution):
          """
          x: x coords of cell
          y: y coords of cell
          z: matrix of values for each (x,y)
          resolution: spatial resolution of each cell
          """
          polygons = []
          values = []
          half_res = resolution / 2
          for i, j  in itertools.product(range(len(x)), range(len(y))):
              minx, maxx = x[i] - half_res, x[i] + half_res
              miny, maxy = y[j] - half_res, y[j] + half_res
              #polygons.append(Polygon([(minx, miny), (minx, maxy), (maxx, maxy), (maxx, miny)]))
              polygons.append(Polygon([(miny, minx), (miny, maxx), (maxy, maxx), (maxy, minx)]))
              if isinstance(z, (int, float)):
                  values.append(z)
              else:
                  values.append(z[j, i])
          return polygons, values

    y_train_df = pd.DataFrame(y_train, columns=[target_variable])

    train_data = pd.concat([X_train, y_train_df], axis=1)

    train_data.shape

    polygons, values = pixel2poly(gridx, gridy, z, resolution)
    tave_model = (gpd.GeoDataFrame({target_variable: values}, geometry=polygons, crs="EPSG:3347")
                      #.to_crs("EPSG:4326")
                      )
    fig = px.choropleth_mapbox(tave_model, geojson=tave_model.geometry, locations=tave_model.index,
                              color=target_variable, color_continuous_scale="RdYlGn_r", opacity=0.5,
                              center={"lat": train_data.Latitude.mean(), "lon": train_data.Longitude.mean()}, zoom=3.5,
                              mapbox_style="carto-positron")
    fig.update_layout(margin=dict(l=0, r=0, t=30, b=10))
    fig.update_traces(marker_line_width=1)
    return (fig,fig)

# Step 9: Run the app
if __name__ == '__main__':
    app.run_server(debug=True)