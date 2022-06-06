(function (d3,topojson) {
  'use strict';

  const svg = d3.select('svg');

  const projection = d3.geoMercator();
  const pathGenerator = d3.geoPath().projection(projection);

  d3.json('https://unpkg.com/world-atlas@1.1.4/world/110m.json')
    .then(data => {
      const countries = topojson.feature(data, data.objects.countries);
      svg.selectAll('path').data(countries.features)
        .enter().append('path')
          .attr('d', pathGenerator);
    });

}(d3,topojson));
