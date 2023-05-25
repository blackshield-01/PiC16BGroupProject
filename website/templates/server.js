const express = require('express');
const app = express();
const port = 3000;

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Handle flight search form submission
app.post('/search', (req, res) => {
  const { departure, destination, date } = req.body;

  // Do further processing with the flight search parameters
  // such as calling the machine learning model for predictions

  // Example response to confirm parameter retrieval
  res.send(`Search Parameters: Origin - ${departure}, Destination - ${destination}, Date - ${date}`);
});

// Serve the HTML file
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/results.html');
});

// Start the server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
