document.addEventListener('DOMContentLoaded', (event) => {
    var map = L.map('mapid').setView([51.505, -0.09], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(map);

    var marker;

    function setLatLng(lat, lng) {
        console.log('Setting latitude:', lat);
        console.log('Setting longitude:', lng);
        document.getElementById('id_latitude').value = lat;
        document.getElementById('id_longitude').value = lng;
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

    document.getElementById('postForm').addEventListener('submit', function(event) {
        var lat = document.getElementById('id_latitude').value;
        var lng = document.getElementById('id_longitude').value;
        console.log('Submitting latitude:', lat);
        console.log('Submitting longitude:', lng);
        if (!lat || !lng) {
            event.preventDefault();
            alert("Please select a location on the map.");
        }else {
            // Ensure the form values are set before submitting
            document.getElementById('id_latitude').value = lat;
            document.getElementById('id_longitude').value = lng;
        }
    });
});