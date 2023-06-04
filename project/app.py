from flask import Flask, request, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('flight_price_analysis.pkl', 'rb'))  # loading the model

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    """Grabs the input values and uses them to make prediction"""
    duration = int(request.form["duration"])
    stops = int(request.form["stops"])
    prediction = model.predict([[duration, stops]])  # this returns a list e.g. [127.20488798], so pick first element [0]
    output = round(prediction[0], 2) 

    return render_template('index.html', prediction_text=f'A flight of {duration} min and with {stops} stops has a predicted cost of ${output}')
  
if __name__ == "__main__":
    app.run(port=7000)