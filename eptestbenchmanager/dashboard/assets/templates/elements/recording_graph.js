var {{ data.uid }}_socket = io('{{ data.namespace }}');
var {{ data.uid }}_element = document.getElementById('{{ data.uid }}_graph');
var {{ data.uid }}_data = [{
    x: [],
    y: [],
    mode: 'lines+markers'
}];
var {{ data.uid }}_layout = {
    title: '{{ data.uid }} Graph',
    xaxis: {
        title: 'horizontal axis'
    },
    yaxis: {
        title: 'vertical axis'
    }
};


{{ data.uid }}_socket.on('update', function(data) {
    {{ data.uid }}_data[0].x = data.h_axis_data;
    {{ data.uid }}_data[0].y = data.v_axis_data;
    Plotly.newPlot({{ data.uid }}_element, {{ data.uid }}_data, {{ data.uid }}_layout);
});

{{ data.uid }}_socket.on('append_point', function(data) {
    if ('{{ data.rolling }}' == 'True') {
        Plotly.extendTraces({{ data.uid }}_element, {
        x: [[data.h_axis_datapoint]],
        y: [[data.v_axis_datapoint]]
    }, [0], {{ data.max_points }});
    } else {
            
        Plotly.extendTraces({{ data.uid }}_element, {
            x: [[data.h_axis_datapoint]],
            y: [[data.v_axis_datapoint]]
        }, [0]);
    }
});


