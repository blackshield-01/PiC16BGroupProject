# Flight Ticket Price Prediction
In this project, our aim is to help users determine the cheapest time to travel by predicting what the cost of their flight ticket will be.
To accomplish this, we scraped our price data from Kayak and used it to train our machine learning model to predict the price of flight tickets. We also created a user-friendly website where users can input their preferences to access our model.

For our dataset, we will be focusing on the time period from June 1st 2023 to August 31st 2023.
Our flights will depart from LAX and arrive at the following airports : HNL, JFK, DEN, DFW, SFO, CHI, ATL.

For our code, we have separated them into several files:
1. webscraping_selenium.ipynb - web scraping
2. preprocessing.py - cleaning our data and data visualizations
3. airport_visualization.ipynb - additional visualizations
4. sklearn_modeling.ipynb - machine learning model
5. tensorflow_modeling.ipynb - neural network
6. website folder - all the files needed to load the website

To run the website, save the sklearn_modeling.ipynb as a pickle file and download the entire website folder along with the app.py file and store them in the same folder!!!
1. Open all the files on your computer and run the index.html and style.css files
2. Create a virtual environment by entering 'python3 -m venv deploy-mlmodel-env' into your terminal
3. Locate your app.py file in your terminal
4. Run your app.py script
5. Enter 'python app.py' into your terminal
6. A message with the link http://127.0.0.1:5000 should appear
7. Copy and paste the link into your browser and the website should be fully functional and return your predicted prices and some visualizations

If any of these steps do not work, we used https://towardsdatascience.com/how-to-easily-build-your-first-machine-learning-web-app-in-python-c3d6c0f0a01c as our guideline and it might help you out as well!
