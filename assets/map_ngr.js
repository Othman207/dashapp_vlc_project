window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        large_params_function: function(id,json) {
          const H = Highcharts,
               map = H.maps['countries/ne/ne-all'];
          const data = json.map(v => {
            v.z = v.volume;
            return v;
          });

          Highcharts.mapChart(id, {
            title: {
                text: 'Map Showing Volume of Vaccines for 2021 in Dosso Region'
            },
            tooltip: {
              pointFormat: '{point.name}<br>' +
                  'Total Volume (L): {point.volume}',
              valueDecimals: 2
            },

            mapNavigation: {
                enabled: true
            },
            credits: {
              enabled: false
            },

            series: [{
                // Use the gb-all map with no data as a basemap
                name: 'Basemap',
                mapData: map,
                borderColor: '#606060',
                nullColor: 'rgba(200, 200, 200, 0.2)',
                showInLegend: false
            }, {
                name: 'Separators',
                type: 'mapline',
                data: H.geojson(map, 'mapline'),
                nullColor: '#707070',
                color: '#101010',
                showInLegend: false,
                enableMouseTracking: false
            }, {
                // Specify points using lat/lon
                type: 'mapbubble',
                name: 'Districts',
                dataLabels: {
                  enabled: true,
                  format: '{point.name}'
                },
                color: Highcharts.getOptions().colors[0],
                data: data,
                maxSize: '12%'
            },
            {
              type: 'mappoint',
              color: Highcharts.getOptions().colors[1],
              showInLegend: false,
              enableMouseTracking: false,
              data: [{
                name: 'Tillabéri',
                lat: 14.206129363979821,
                lon: 1.4579102917595341
              },
              {
                name: 'Tahoua',
                lat: 14.890321067620881,
                lon: 5.25799711948009
              },
              {
                name: 'Maradi',
                lat: 13.500988374783423,
                lon: 7.103621178249017
              },
              {
                name: 'Zinder',
                lat: 13.801729206692505,
                lon: 8.985117605776155
              },
              {
                name: 'Diffa',
                lat: 13.676170548970694,
                lon: 12.71150688024504
              },
              {
                name: 'Agadez',
                lat: 16.974207387399353,
                lon: 7.986493690686179
              },
              {
                name: 'Dosso',
                lat:13.050546691115104,
                lon:3.208135897880922
              }]
            }
          ]
        });

        }
    }
});
