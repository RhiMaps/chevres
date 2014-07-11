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

var chevresLayer = L.geoCsv(null, {
    firstLineTitles: true,
    fieldSeparator: ',',
    onEachFeature: function (feature, layer) {
        var popupContent= '<b>'+feature.properties['name']+'</b>'+
                          '<img src="./datas/'+feature.properties['imgpath']+'"/>';
        var popup = L.popup( {minWidth: '400'}).setContent(popupContent);
        //for (var key in feature.properties) {
        //    var title = chevresLayer.getPropertyTitle(key);
        //    popup += '<b>'+title+'</b><br />'+feature.properties[key]+'<br />';
        //}
        
        layer.bindPopup(popup);
    },
});


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
    },
   complete: function() {
      //$('#cargando').delay(500).fadeOut('slow');
   }
});


  var baseLayers = {
    "OSM": osmLayer
  };

var overLays = {
    "chevres": chevresLayer,
};

L.control.layers(baseLayers, overLays).setPosition('topright').addTo(map);
