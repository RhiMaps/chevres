var z = 4;
var myLL = L.latLng(43.808, 0.887);

// create a map in the "map" div, set the view to a given place and zoom
var map = L.map('map', {
    center: myLL,
    zoom: z
});


// add an OpenStreetMap tile layer
var osmLayer = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: 'OpenStreetMap'
}).addTo(map);

var chevresLayer = L.geoCsv(null, {
    firstLineTitles: true,
    fieldSeparator: ',',
    onEachFeature: function(feature, layer) {
        var popupContent = '<b>' + feature.properties['name'] + '</b>';
       if ( feature.properties['poids']) popupContent +='</br>'+ feature.properties['poids'] + ' gr.';
       if ( feature.properties['grasse']) popupContent +='</br>'+ feature.properties['grasse'] + '% mat. grasse';
                            //+ '<img src="./datas/' + feature.properties['imgpath'] + '"/>';
        var popup = L.popup({
            minWidth: '400'
        }).setContent(popupContent);
        //for (var key in feature.properties) {
        //    var title = chevresLayer.getPropertyTitle(key);
        //    popup += '<b>'+title+'</b><br />'+feature.properties[key]+'<br />';
        //}
        layer.bindPopup(popup);
    },
    pointToLayer: function(feature, latlng) {
        var myIcon = L.icon({
            iconUrl: 'images/chevre.png',
            iconSize: [40, 40],
            iconAnchor: [20, 20],
            popupAnchor: [0, -20]
        });
        var marker = L.marker(latlng, {
            icon: myIcon
        });
        return marker;
    },
});


$.ajax({
    type: 'GET',
    dataType: 'text',
    url: 'datas/chevres_vincent_geocoded.csv',
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

// rewrite url to show lat/lon/zoom
// (uses leaflet-hash plugin as submodule)
var hash = new L.Hash(map);
