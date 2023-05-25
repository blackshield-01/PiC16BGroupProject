// Redirects the index.html page to the results.html page
document.getElementById('flightForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission behavior
    window.location.href = this.action; // Redirect to the specified action (results.html)
  });