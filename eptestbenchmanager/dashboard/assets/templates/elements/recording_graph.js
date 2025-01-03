var {{ uid }}_socket = io('/{{ data.namespace }}');
var {{ uid }}_element = document.getElementById('{{ uid }}_graph');
var {{ uid }}_data = {
    horizontal: [],
    vertical: [],
    mode = 'lines+markers'
};
var {{ uid }}_layout = {
    title: '{{ data.uid }} Graph',
    xaxis: {
        title: 'horizontal axis'
    },
    yaxis: {
        title: 'vertical axis'
    }
};


{{ uid }}_socket.on('update', function(data) {
    {{ uid }}_data.horizontal = data.h_axis_data;
    {{ uid }}_data.vertical = data.v_axis_data;
    Plotly.newPlot({{ uid }}_element, {{ uid }}_data, {{ uid }}_layout);
});

{{ uid }}_socket.on('append_point', function(data) {
    Plotly.extendTraces({{ uid }}_element, {
        x: [[data.h_axis_datapoint]],
        y: [[data.v_axis_datapoint]]
    }, [0]);
});


