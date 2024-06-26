// Function to fetch data from Django API endpoint
function fetchDataAndRender() {
    fetch('/dashboard/api/data/')
        .then(response => response.json())
        .then(data => {
            renderCharts(data); // Call function to render charts with fetched data
        });
}

// Function to render charts with D3.js
function renderCharts(data) {
    renderBarChart(data);
    renderPieChart(data);
}

// Function to render bar chart
function renderBarChart(data) {
    const svg = d3.select('#bar-chart'),
        margin = { top: 30, right: 30, bottom: 70, left: 60 },
        width = +svg.attr('width') - margin.left - margin.right,
        height = +svg.attr('height') - margin.top - margin.bottom;

    const x = d3.scaleBand()
        .range([margin.left, width - margin.right])
        .padding(0.1)
        .domain(data.map(d => d.topic));

    const y = d3.scaleLinear()
        .range([height - margin.bottom, margin.top])
        .domain([0, d3.max(data, d => d.intensity)]);

    svg.append('g')
        .attr('transform', `translate(0,${height - margin.bottom})`)
        .call(d3.axisBottom(x))
        .selectAll('text')
        .style('text-anchor', 'end')
        .attr('dx', '-.8em')
        .attr('dy', '-.55em')
        .attr('transform', 'rotate(-45)');

    svg.append('g')
        .attr('transform', `translate(${margin.left},0)`)
        .call(d3.axisLeft(y));

    svg.selectAll('.bar')
        .data(data)
        .enter().append('rect')
        .attr('class', 'bar')
        .attr('x', d => x(d.topic))
        .attr('width', x.bandwidth())
        .attr('y', d => y(d.intensity))
        .attr('height', d => height - margin.bottom - y(d.intensity))
        .on('mouseover', function() {
            d3.select(this).attr('fill', '#4CAF50');
        })
        .on('mouseout', function() {
            d3.select(this).attr('fill', 'steelblue');
        });
}

// Function to render pie chart
function renderPieChart(data) {
    const svg = d3.select('#pie-chart'),
        width = +svg.attr('width'),
        height = +svg.attr('height'),
        radius = Math.min(width, height) / 2,
        g = svg.append('g').attr('transform', `translate(${width / 2},${height / 2})`);

    const color = d3.scaleOrdinal()
        .domain(data.map(d => d.topic))
        .range(d3.schemeCategory10);

    const pie = d3.pie().value(d => d.intensity);
    const path = d3.arc()
        .outerRadius(radius - 10)
        .innerRadius(0);

    const arc = g.selectAll('.arc')
        .data(pie(data))
        .enter().append('g')
        .attr('class', 'arc');

    arc.append('path')
        .attr('d', path)
        .attr('class', 'pie-slice')
        .attr('fill', d => color(d.data.topic))
        .on('mouseover', function() {
            d3.select(this).attr('fill', '#FBC02D');
        })
        .on('mouseout', function(d) {
            d3.select(this).attr('fill', color(d.data.topic));
        });

    arc.append('text')
        .attr('transform', d => `translate(${path.centroid(d)})`)
        .attr('dy', '0.35em')
        .text(d => d.data.topic);
}

// Load data and render charts on page load
document.addEventListener('DOMContentLoaded', function() {
    fetchDataAndRender();
});
