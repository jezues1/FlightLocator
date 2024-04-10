document.addEventListener('DOMContentLoaded', function() {
    // Add event listener to the search form submission
    document.querySelector('form').addEventListener('submit', function(event) {
        event.preventDefault();
        const origin = document.querySelector('input[name="origin"]').value;
        const destination = document.querySelector('input[name="destination"]').value;
        const date = document.querySelector('input[name="date"]').value;
        
        // Make an AJAX request to the server
        fetch(`/search?origin=${origin}&destination=${destination}&date=${date}`)
            .then(response => response.json())
            .then(data => {
                // Update the search results on the page
                const searchResults = document.querySelector('#search-results');
                searchResults.innerHTML = '';
                
                if (data.length > 0) {
                    data.forEach(flight => {
                        const li = document.createElement('li');
                        li.innerHTML = `
                            Flight Number: ${flight.flight.number}<br>
                            Airline: ${flight.airline.name}<br>
                            Departure: ${flight.departure.airport} (${flight.departure.scheduled})<br>
                            Arrival: ${flight.arrival.airport} (${flight.arrival.scheduled})<br>
                            <a href="/add_favorite/${flight.flight.number}">Add to Favorites</a>
                        `;
                        searchResults.appendChild(li);
                    });
                } else {
                    searchResults.innerHTML = '<p>No flights found.</p>';
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});