var z = 7;
var myLL = L.latLng(46.725,1.785);


// create a map in the "map" div, set the view to a given place and zoom
var map = L.map('map', {
    center: myLL,
    zoom: z
});


// add an OpenStreetMap tile layer
var osmLayer = L.tileLayer('https://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: 'OpenStreetMap'
}).addTo(map);

var esriLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
});

var mapqLayer = L.tileLayer('https://{s}.mqcdn.com/tiles/1.0.0/osm/{z}/{x}/{y}.png', {
    attribution: 'MapQuest OpenStreetMap',
    subdomains: ['otile1', 'otile2', 'otile3', 'otile4']
});


var chevresLayer = L.geoCsv(null, {
    firstLineTitles: true,
    fieldSeparator: ';',
    onEachFeature: function(feature, layer) {
        var popupContent = '<b>' + feature.properties['name'] + '</b></br>';
        if (feature.properties['poids']) popupContent += ' ' + feature.properties['poids'] + ' gr.';
        if (feature.properties['grasse']) popupContent += ' ' + feature.properties['grasse'] + '% M. G.';
        if (feature.properties['ferme']) popupContent += '</br>' + feature.properties['ferme'];
        if (feature.properties['code']) popupContent += '</br>' + feature.properties['code'];
        if (feature.properties['ville']) popupContent += ' ' + feature.properties['ville'];
        if (feature.properties['imgpath']){
            popupContent += '<img class="chevre" src="./datas/' + feature.properties['imgpath'] + '"/>';
        }else{
            popupContent += '<img class="chevre" src="./images/chevre.png"/>';
        }
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
        if (feature.properties['imgpath']){
            iconUrl = 'images/chevre.png'
        }else{
            iconUrl = 'images/chevre-rouge.png'
        }
        var myIcon = L.icon({
            iconUrl: iconUrl,
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
    url: 'datas/chevres.csv',
    error: function() {
        alert('Chargement impossible');
    },
    success: function(csv) {
        //var cluster = new L.MarkerClusterGroup();
        chevresLayer.addData(csv);
        //cluster.addLayer(bankias);
        //map.addLayer(cluster);
        map.addLayer(chevresLayer);
        //map.fitBounds(chevresLayer.getBounds());
    },
    complete: function() {
        //$('#cargando').delay(500).fadeOut('slow');
    }
});


var baseLayers = {
    "Satellite": esriLayer,
    "OSM": osmLayer,
    "MapBox": mapqLayer,
};

var overLays = {
    "chevres": chevresLayer,
};

// Layers switchers
L.control.layers(baseLayers, overLays).setPosition('topright').addTo(map);

// Scale at bottom left
L.control.scale().addTo(map);

// Rewrite url to show lat/lon/zoom
// (uses leaflet-hash plugin as submodule)
var hash = new L.Hash(map);

// search field to find place
// (use leaflet-geocoding plugin as submodule)
new L.Control.GeoSearch({
    provider: new L.GeoSearch.Provider.OpenStreetMap(),
    zoomLevel: 15,
}).addTo(map);
