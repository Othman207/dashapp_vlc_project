var wms_layers = [];


        var lyr_OSMStandard_0 = new ol.layer.Tile({
            'title': 'OSM Standard',
            'type': 'base',
            'opacity': 1.000000,
            
            
            source: new ol.source.XYZ({
    attributions: ' &middot; <a href="https://www.openstreetmap.org/copyright">© OpenStreetMap contributors, CC-BY-SA</a>',
                url: 'http://tile.openstreetmap.org/{z}/{x}/{y}.png'
            })
        });
var format_Axesdirections_1 = new ol.format.GeoJSON();
var features_Axesdirections_1 = format_Axesdirections_1.readFeatures(json_Axesdirections_1, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_Axesdirections_1 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_Axesdirections_1.addFeatures(features_Axesdirections_1);
var lyr_Axesdirections_1 = new ol.layer.Vector({
                declutter: true,
                source:jsonSource_Axesdirections_1, 
                style: style_Axesdirections_1,
                interactive: true,
                title: '<img src="styles/legend/Axesdirections_1.png" /> Axes directions'
            });
var format_DeliveryLocations_2 = new ol.format.GeoJSON();
var features_DeliveryLocations_2 = format_DeliveryLocations_2.readFeatures(json_DeliveryLocations_2, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_DeliveryLocations_2 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_DeliveryLocations_2.addFeatures(features_DeliveryLocations_2);
var lyr_DeliveryLocations_2 = new ol.layer.Vector({
                declutter: true,
                source:jsonSource_DeliveryLocations_2, 
                style: style_DeliveryLocations_2,
                interactive: true,
                title: '<img src="styles/legend/DeliveryLocations_2.png" /> Delivery Locations'
            });
var format_Districts_3 = new ol.format.GeoJSON();
var features_Districts_3 = format_Districts_3.readFeatures(json_Districts_3, 
            {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:3857'});
var jsonSource_Districts_3 = new ol.source.Vector({
    attributions: ' ',
});
jsonSource_Districts_3.addFeatures(features_Districts_3);
var lyr_Districts_3 = new ol.layer.Vector({
                declutter: true,
                source:jsonSource_Districts_3, 
                style: style_Districts_3,
                interactive: true,
                title: '<img src="styles/legend/Districts_3.png" /> Districts'
            });

lyr_OSMStandard_0.setVisible(true);lyr_Axesdirections_1.setVisible(true);lyr_DeliveryLocations_2.setVisible(true);lyr_Districts_3.setVisible(true);
var layersList = [lyr_OSMStandard_0,lyr_Axesdirections_1,lyr_DeliveryLocations_2,lyr_Districts_3];
lyr_Axesdirections_1.set('fieldAliases', {'DIST_KM': 'DIST_KM', 'DURATION_H': 'DURATION_H', 'PROFILE': 'PROFILE', 'PREF': 'PREF', 'OPTIONS': 'OPTIONS', 'FROM_ID': 'FROM_ID', 'TO_ID': 'TO_ID', });
lyr_DeliveryLocations_2.set('fieldAliases', {'id': 'id', 'name': 'name', 'ORIG_FID': 'ORIG_FID', });
lyr_Districts_3.set('fieldAliases', {'id': 'id', 'Name': 'Name', 'ORIG_FID': 'ORIG_FID', });
lyr_Axesdirections_1.set('fieldImages', {'DIST_KM': 'TextEdit', 'DURATION_H': 'TextEdit', 'PROFILE': 'TextEdit', 'PREF': 'TextEdit', 'OPTIONS': 'TextEdit', 'FROM_ID': 'TextEdit', 'TO_ID': 'TextEdit', });
lyr_DeliveryLocations_2.set('fieldImages', {'id': 'TextEdit', 'name': 'TextEdit', 'ORIG_FID': 'TextEdit', });
lyr_Districts_3.set('fieldImages', {'id': 'TextEdit', 'Name': 'TextEdit', 'ORIG_FID': 'TextEdit', });
lyr_Axesdirections_1.set('fieldLabels', {'DIST_KM': 'no label', 'DURATION_H': 'no label', 'PROFILE': 'no label', 'PREF': 'no label', 'OPTIONS': 'no label', 'FROM_ID': 'no label', 'TO_ID': 'no label', });
lyr_DeliveryLocations_2.set('fieldLabels', {'id': 'inline label', 'name': 'no label', 'ORIG_FID': 'no label', });
lyr_Districts_3.set('fieldLabels', {'id': 'header label', 'Name': 'header label', 'ORIG_FID': 'no label', });
lyr_Districts_3.on('precompose', function(evt) {
    evt.context.globalCompositeOperation = 'normal';
});