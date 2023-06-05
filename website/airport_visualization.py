import plotly.express as px
import pandas as pd

destinations = ['ATL', 'CHI', 'DEN', 'DFW', 'HNL', 'JFK', 'SFO']

flights = pd.DataFrame()
for dest in destinations:
    
    flights = pd.concat([flights, pd.read_csv(f'flight_LAX_{dest}_data_0601_0831.csv')])
    
flights.to_csv('flights.csv', index = False)

airports = pd.read_csv('airport-codes_csv.csv')


destinations = set(flights['Destination'])
destinations.add('LAX')

airports = airports[['name', 'iata_code', 'coordinates']]
airports = airports.rename({'name' : 'Airport', 
                            'iata_code' : 'Destination'},
                           axis = 1)


airports = airports[airports['Destination'].isin(destinations)]


airports['longitude'] = airports['coordinates'].str.split(', ').str[0].astype(float)
airports['latitude'] = airports['coordinates'].str.split(', ').str[1].astype(float)

LAX_lon = airports[airports['Destination'] == 'LAX']['longitude'].iloc[0]
LAX_lat = airports[airports['Destination'] == 'LAX']['latitude'].iloc[0]

airports = airports[airports['Destination'] != 'LAX']

airports.to_csv('airports.csv', index = False)


def visualize_airports(airports, flights, metric):
    
    lons = []
    lats = []

    for lon in airports['longitude']:

        lons.append(lon)
        lons.append(LAX_lon)

    for lat in airports['latitude']:

        lats.append(lat)
        lats.append(LAX_lat)
        
    colors = flights.groupby('Destination')['Price'].aggregate([metric])
    metric_name = colors.columns[0]
    colors = list(colors[metric_name])
    
    #error handling for single airport visualizations
    if (len(colors) != len(airports['longitude'])):
        colors = [0]
    
    fig1 = px.scatter_mapbox(airports,
                             lat = 'latitude',
                             lon = 'longitude',
                             color = colors,
                             hover_data = {'latitude' : False,
                                           'longitude' : False},
                             labels = {'color' : metric_name},
                             hover_name = 'Airport')
    
    fig2 = px.scatter_mapbox(lon = [LAX_lon],
                             lat = [LAX_lat],
                             hover_name = ['Los Angeles International Airport']).add_traces(fig1.data)
    
    fig3 = px.line_mapbox(airports,
                          lat = lats,
                          lon = lons,
                          color_discrete_sequence = ['red'],
                          zoom = 2,
                          mapbox_style = 'carto-positron').add_traces(fig2.data)
    
    fig3.update_traces(marker={'size' : 20,
                               'opacity' : .5})

    return fig3