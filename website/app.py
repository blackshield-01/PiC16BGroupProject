from flask import Flask, request, render_template
import pickle
import json
import plotly
import airport_visualization as av
import pandas as pd
import numpy as np
import preprocessing
from datetime import datetime
#from sklearn.preprocessing import LabelEncoder

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


@app.route('/')
def home():
    
    fig = av.visualize_airports(airports, 
                                flights, 
                                metric = np.mean)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('index.html', graphJSON = graphJSON)

@app.route('/predict',methods=['POST'])
def predict():
    """Grabs the input values and uses them to make prediction"""
    companyname = int(request.form["companyname"])    
    destination = int(request.form["destination"])
    date = request.form["date"]
    duration = int(request.form["duration"])
    stops = int(request.form["stops"])
    
    #perform preprocessing on destination and date
    date = datetime.strptime(date, '%Y-%m-%d')
    dayofweek = date.weekday() + 1
    month = date.month
    date = (date - datetime(2023, 6, 1)).days
    
    prediction = model.predict([[companyname, 
                                 stops, 
                                 duration,
                                 destination, 
                                 date, 
                                 dayofweek, 
                                 month]])  # this returns a list e.g. [127.20488798], so pick first element [0]
    output = round(prediction[0], 2) 
    
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
    
    destination = dest_encoding[destination]
    
    df = flights[(flights['Duration'] >= duration - 90) & (flights['Duration'] <= duration + 90)]
    df = df[flights['Stops'] == stops]
    df = df[flights['Destination'] == destination]
    df = df[flights['Date'] == date]
    df = df[flights['Company Name'] == companyname]

    fig = av.visualize_airports(airports[airports['Destination'] == destination],
                                df,
                                metric = np.mean)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    df = df[['Price', 'Duration', 'Destination', 'From']]
    
    return render_template('index.html', 
                           prediction_text=f'Predicted cost: ${output}.',
                           graphJSON = graphJSON,
                           tables=[df.to_html(classes='data', header='true')],
                           table_text = 'See example ticket prices here: ')
  
if __name__ == "__main__":
    app.run(port=7000)