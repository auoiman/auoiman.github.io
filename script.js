// Initialize the map
var map = L.map('map').setView([-41.2865, 174.7762], 6);

// Add the base map
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Fetch video data from JSON file
fetch('video_data.json')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Process video data and add markers to map
        data.forEach(video => {
            var marker = L.marker([video.latitude, video.longitude]).addTo(map);
            marker.bindPopup(`<div class="video-popup"><iframe width="250" height="150" src="${video.video_url}" frameborder="0" allowfullscreen></iframe></div>`, {
                minWidth: 250
            });

            // Populate the table
            var tableRow = document.createElement('tr');
            tableRow.innerHTML = `
                <td>${video.title}</td>
                <td><a href="${video.video_url}" target="_blank">Watch Video</a></td>
            `;
            document.getElementById('video-list').appendChild(tableRow);
        });
    })
    .catch(error => console.error('Error fetching video data:', error));
