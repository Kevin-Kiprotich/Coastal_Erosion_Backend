var map=L.map('map').setView([1.65,26.17],4);

var basemap=L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
})
basemap.addTo(map);

L.marker([1.65,26.17]).addTo(map);