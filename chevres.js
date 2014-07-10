var z=11;
var myLL= L.latLng(43.3317,2.5808);


// create a map in the "map" div, set the view to a given place and zoom
var map = L.map('map', {
  center:myLL,
  zoom:z});


// add an OpenStreetMap tile layer
var osmLayer = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
  attribution: 'OpenStreetMap'
  }).addTo(map);


