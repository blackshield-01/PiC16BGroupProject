from flask import Flask, request, render_template
import pickle
import json
import plotly
import airport_visualization as av
import pandas as pd
import numpy as np
import preprocessing
from datetime import datetime

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))  # loading the model

airports = pd.read_csv('airports.csv')
flights = pd.read_csv('flights.csv')

flights['Duration'] = preprocessing.clean_duration(flights['Duration'])
flights['Stops'] = flights['Stops'].apply(preprocessing.clean_stops).astype(float).fillna(-1).astype(int)
flights['Stops'] = flights['Stops'].replace(-1, '')
flights = preprocessing.clean_company_name(flights)
flights = preprocessing.clean_date(flights)
flights = preprocessing.preprocess(flights)

company_encodes = pd.read_csv('company_encodes.csv')

@app.route('/')
def home():
    
    fig = av.visualize_airports(airports, 
                                flights, 
                                metric = np.mean)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('index.html', 
                           graphJSON = graphJSON, 
                           names = list(company_encodes['Company Name']))

@app.route('/predict',methods=['POST'])
def predict():
    """Grabs the input values and uses them to make prediction"""
    companyname = request.form["companyname"]
    destination = int(request.form["destination"])
    date = request.form["date"]
    duration = int(request.form["duration"])
    stops = int(request.form["stops"])
    
    #perform preprocessing on company name and destination
    company_id = company_encodes[company_encodes['Company Name'] == companyname].index[0]
    
    dest_encoding = \
        {
            0:'ATL',
            5:'ORD',
            6:'SFO',
            1:'DEN',
            4:'JFK',
            3:'HNL',
            2:'DFW'
        }
    dest_name = dest_encoding[destination]
    
    #check if company flies to given airport
    df = flights[flights['Destination'] == dest_name]
    df = df[flights['Company Name'] == company_id]
    if (len(df.index) == 0):
        return render_template('index.html',
                               prediction_text='No flights found. Try a different company.',
                               names = list(company_encodes['Company Name']))
    
    #perform preprocessing on company name and date
    companyname = company_encodes[company_encodes['Company Name'] == companyname].index[0]
    
    date = datetime.strptime(date, '%Y-%m-%d')
    dayofweek = date.weekday() + 1
    month = date.month
    date = (date - datetime(2023, 6, 1)).days
    
    prediction = model.predict([[company_id, 
                                 stops, 
                                 duration,
                                 destination, 
                                 date, 
                                 dayofweek, 
                                 month]])  # this returns a list e.g. [127.20488798], so pick first element [0]
    output = round(prediction[0], 2) 
    
    df = df[(flights['Duration'] >= duration - 90) & (flights['Duration'] <= duration + 90)]
    df = df[flights['Date'] == date]
    df = df[flights['Stops'] == stops]
    
    #visualize flight
    fig = av.visualize_airports(airports[airports['Destination'] == dest_name],
                                df,
                                metric = np.mean)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    #example flights
    df = df[['Price', 'Duration', 'Destination', 'From']]
    
    return render_template('index.html',
                           prediction_text=f'Predicted cost: ${output}.',
                           graphJSON = graphJSON,
                           names = list(company_encodes['Company Name']),
                           tables=[df.to_html(classes='data', header='true')],
                           table_text = 'See example ticket prices here: ')
  
if __name__ == "__main__":
    app.run(port=7000)