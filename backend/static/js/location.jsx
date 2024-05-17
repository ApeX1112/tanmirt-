document.addEventListener('DOMContentLoaded', (event) => {
    var map = L.map('mapContainer').setView([51.505, -0.09], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(map);

    var marker;

    function setLatLng(lat, lng) {
        console.log('Setting latitude:', lat);
        console.log('Setting longitude:', lng);
        document.getElementById('profileLatitude').value = lat;
        document.getElementById('profileLongitude').value = lng;
    }

    map.on('click', function(e) {
        if (marker) {
            map.removeLayer(marker);
        }
        marker = L.marker(e.latlng).addTo(map);
        setLatLng(e.latlng.lat, e.latlng.lng);
    });

    map.locate({setView: true, maxZoom: 16});
    map.on('locationfound', function(e) {
        if (marker) {
            map.removeLayer(marker);
        }
        marker = L.marker(e.latlng).addTo(map);
        setLatLng(e.latlng.lat, e.latlng.lng);
    });

    document.getElementById('profilePostForm').addEventListener('submit', function(event) {
        var lat = document.getElementById('profileLatitude').value;
        var lng = document.getElementById('profileLongitude').value;
        console.log('Submitting latitude:', lat);
        console.log('Submitting longitude:', lng);
        if (!lat || !lng) {
            event.preventDefault();
            alert("Please select a location on the map.");
        }
    });
});
