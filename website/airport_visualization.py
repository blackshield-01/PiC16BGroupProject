import plotly.express as px
import pandas as pd

#need LAX coords for plotting
airport_codes = pd.read_csv('airport-codes_csv.csv')

airport_codes = airport_codes[['name', 'iata_code', 'coordinates']]
airport_codes = airport_codes.rename({'name' : 'Airport', 
                                      'iata_code' : 'Destination'},
                                      axis = 1)

airport_codes = airport_codes[airport_codes['Destination'] == 'LAX']

airport_codes['longitude'] = airport_codes['coordinates'].str.split(', ').str[0].astype(float)
airport_codes['latitude'] = airport_codes['coordinates'].str.split(', ').str[1].astype(float)

#get LAX coords
LAX_lon = airport_codes[airport_codes['Destination'] == 'LAX']['longitude'].iloc[0]
LAX_lat = airport_codes[airport_codes['Destination'] == 'LAX']['latitude'].iloc[0]


def visualize_airports(airports, flights, metric):
    '''
    Function plots the given airports and applies the given metric to the flights
    '''
    
    lons = []
    lats = []
    
    #to create lines, create list of lines from each airport to LAX
    for lon in airports['longitude']:
        lons.append(lon)
        lons.append(LAX_lon)
    for lat in airports['latitude']:
        lats.append(lat)
        lats.append(LAX_lat)
    
    #colors airports based on metric
    colors = flights.groupby('Destination')['Price'].aggregate([metric])
    metric_name = colors.columns[0]
    colors = airports.join(colors, on = 'Destination')
    colors = list(colors[metric_name])
    
    #plots each destination
    fig1 = px.scatter_mapbox(airports,
                             lat = 'latitude',
                             lon = 'longitude',
                             color = colors,
                             hover_data = {'latitude' : False,
                                           'longitude' : False},
                             labels = {'color' : metric_name},
                             hover_name = 'Airport')
    #plots LAX airport
    fig2 = px.scatter_mapbox(lon = [LAX_lon],
                             lat = [LAX_lat],
                             hover_name = ['Los Angeles International Airport']).add_traces(fig1.data)
    #plots lines from LAX to each destination
    fig3 = px.line_mapbox(airports,
                          lat = lats,
                          lon = lons,
                          color_discrete_sequence = ['red'],
                          zoom = 2,
                          mapbox_style = 'carto-positron').add_traces(fig2.data)
    
    fig3.update_traces(marker={'size' : 20,
                               'opacity' : .5})

    return fig3