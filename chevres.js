var z=4;
var myLL= L.latLng(36.17,-91.10);


// create a map in the "map" div, set the view to a given place and zoom
var map = L.map('map', {
  center:myLL,
  zoom:z});


// add an OpenStreetMap tile layer
var osmLayer = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
  attribution: 'OpenStreetMap'
  }).addTo(map);

var chevresLayer = L.geoCsv(null, { firstLineTitles: true, fieldSeparator: ',', });


$.ajax ({
    type:'GET',
    dataType:'text',
    url:'datas/chevres.csv',
   error: function() {
     alert('Chargement impossible');
   },
    success: function(csv) {
      //var cluster = new L.MarkerClusterGroup();
        chevresLayer.addData(csv);
        //cluster.addLayer(bankias);
        //map.addLayer(cluster);
        map.addLayer(chevresLayer);
        map.fitBounds(chevresLayer.getBounds());
      alert( 'success');
    },
   complete: function() {
      //$('#cargando').delay(500).fadeOut('slow');
      alert( 'complet');
   }
});


  var baseLayers = {
    "OSM": osmLayer
  };

var overLays = {
    "chevres": chevresLayer,
};

L.control.layers(baseLayers, overLays).setPosition('topright').addTo(map);
