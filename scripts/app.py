import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import random

# Mock data
def read_data(file_path='data/temperature.csv'):
    years = list(range(2010, 2016))
    locations = [(49.28, -123.12), (50.11, -122.95), (53.73, -123.37),
                 (51.04, -114.07), (52.13, -125.75), (54.32, -128.67)]

    data = {'Year': [], 'Latitude': [], 'Longitude': [], 'Temperature': []}

    for year in years:
        for lat, lon in locations:
            data['Year'].append(year)
            data['Latitude'].append(lat)
            data['Longitude'].append(lon)
            data['Temperature'].append(random.uniform(5, 20))
    return data

df = pd.DataFrame(read_data())

# Create a Dash web application
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Temperature Measurement in British Columbia"),
    dcc.Slider(
        id='year-slider',
        min=min(df['Year']),
        max=max(df['Year']),
        value=min(df['Year']),
        marks={str(year): str(year) for year in df['Year'].unique()},
        step=None
    ),
    dcc.Graph(id='temperature-map', config={'scrollZoom': False}),
    dcc.Graph(id='temperature-trend'),
])

# Callback for updating the temperature trend graph
@app.callback(
    Output('temperature-trend', 'figure'),
    Input('temperature-map', 'clickData'),
    Input('year-slider', 'value')
)

def update_temperature_trend(clickData, selected_year):
    if clickData is not None:
        # Extract the clicked point's coordinates
        clicked_point = clickData['points'][0]
        latitude = clicked_point['lat']
        longitude = clicked_point['lon']

        # Filter data for the clicked point
        filtered_data = df[(df['Latitude'] == latitude) & (df['Longitude'] == longitude)]

        fig = px.line(
            filtered_data,
            x='Year',
            y='Temperature',
            title=f'Temperature Trend for Latitude {latitude}, Longitude {longitude}',
            markers=True,
        )

        # Highlight the current year with a red line
        fig.update_traces(line=dict(color='blue'))
        markerColors = ['blue' if year != selected_year else 'red' for year in filtered_data['Year']]
        fig.update_traces(marker=dict(color=markerColors))

        return fig

    return {}

# Callback for updating the temperature map
@app.callback(
    Output('temperature-map', 'figure'),
    Input('year-slider', 'value')
)

def update_temperature_map(selected_year):
    filtered_data = df[df['Year'] == selected_year]
    fig = px.scatter_geo(
        filtered_data,
        lat='Latitude',
        lon='Longitude',
        color='Temperature',
    )

    fig.update_geos(showcoastlines=True,
                    coastlinecolor="Black",
                    showland=True,
                    landcolor="white",
                    # set center as centre of BC
                    center=dict(lat=53.7267, lon=-127.6476),
                    # restrict box to the locations in the data
                    fitbounds="locations",)

    fig.update_layout(title='Temperature Measurement in British Columbia')

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
