var {{ data.uid }}_socket = io('{{ data.namespace }}');
var {{ data.uid }}_element = document.getElementById('{{ data.uid }}_graph');
var {{ data.uid }}_data = [{
    x: [],
    y: [],
    mode: 'lines+markers',
    text: [], // Custom hover text
    hovertemplate: '<b>%{text}</b><br>Time: %{x}<br>Value: %{y}<extra></extra>' // Customize hover
}];

var {{ data.uid }}_layout = {
    title: '{{ data.name }} Graph',
    xaxis: {
        title: 'Time',
        color: '#dadada',
        gridcolor: '#333333',
        zerolinecolor: '#dadada',
        tickmode: 'auto', // Initially auto
    },
    yaxis: {
        title: '{{data.measurement_name}} ({{ data.measurement_unit }})',
        color: '#dadada',
        gridcolor: '#333333',
        zerolinecolor: '#dadada',
    },
    paper_bgcolor: '#111111',
    plot_bgcolor: '#111111',
    font: {
        color: '#dadada'
    }
};

// Function to dynamically determine tick values and custom labels
function remapTickLabels(data) {
    const xValues = data.h_axis_data;
    const labels = data.labels || data.h_axis_data;

    // Determine appropriate ticks (e.g., every nth value for clarity)
    const step = Math.ceil(xValues.length / 10); // Adjust density as needed
    const tickvals = xValues.filter((_, i) => i % step === 0);
    const ticktext = tickvals.map((val) => {
        const index = xValues.indexOf(val);
        return index !== -1 ? labels[index] : val;
    });

    return { tickvals, ticktext };
}

function formatRelativeTime(timestamp) {
    const now = Date.now();
    const delta = now - timestamp * 1000; // Convert seconds to milliseconds
    const deltaInSeconds = Math.floor(delta / 1000);
    
    const days = Math.floor(deltaInSeconds / (24 * 3600));
    const hours = Math.floor((deltaInSeconds % (24 * 3600)) / 3600);
    const minutes = Math.floor((deltaInSeconds % 3600) / 60);
    const seconds = deltaInSeconds % 60;
    const millis = delta % 1000;

    if (days > 0) {
        return `T-${days} days, ${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}.${String(millis).padStart(3, '0')}`;
    } else {
        return `T-${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}.${String(millis).padStart(3, '0')}`;
    }
}

function formatAbsoluteTime(timestamp) {
    const absTime = timestamp - {{ data.t0 }}; // Absolute time difference in seconds

    const days = Math.floor(absTime / 86400);
    const hours = Math.floor((absTime % 86400) / 3600);
    const minutes = Math.floor((absTime % 3600) / 60);
    const seconds = Math.floor(absTime % 60);
    const millis = Math.floor((absTime * 1000) % 1000);

    if (days > 0) {
        return `T+${days} days, ${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}.${String(millis).padStart(3, '0')}`;
    } else {
        return `T+${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}.${String(millis).padStart(3, '0')}`;
    }
}


function generateLabel(timestamp) {
    if ('{{ data.rolling }}' == 'True') { 
        return formatRelativeTime(timestamp);
    }
    else {
        return formatAbsoluteTime(timestamp);
    }
}


{{ data.uid }}_socket.on('update', function(data) {
    {{ data.uid }}_data[0].x = data.h_axis_data; // Original timestamps
    {{ data.uid }}_data[0].y = data.v_axis_data;
    {{ data.uid }}_data[0].text = data.h_axis_data.map(generateLabel) || data.h_axis_data; // Custom hover labels

    // Generate tickvals and ticktext
    const { tickvals, ticktext } = remapTickLabels(data);

    // Update layout with remapped ticks
    {{ data.uid }}_layout.xaxis.tickvals = tickvals;
    {{ data.uid }}_layout.xaxis.ticktext = ticktext;
    {{ data.uid }}_layout.xaxis.tickmode = 'array'; // Explicitly set tickmode to array

    Plotly.newPlot({{ data.uid }}_element, {{ data.uid }}_data, {{ data.uid }}_layout);
});

{{ data.uid }}_socket.on('append_point', function(data) {
    const newPoint = {
        x: [[data.h_axis_datapoint]],
        y: [[data.v_axis_datapoint]],
        text: [[generateLabel(data.h_axis_datapoint) || data.h_axis_datapoint]] // Add hover label
    };

    if ('{{ data.rolling }}' == 'True') {
        Plotly.extendTraces({{ data.uid }}_element, newPoint, [0], {{ data.max_points }});
    } else {
        Plotly.extendTraces({{ data.uid }}_element, newPoint, [0]);
    }

    // Update tick values and labels for new data
    const xValues = {{ data.uid }}_data[0].x;
    const labels = {{ data.uid }}_data[0].text;

    const { tickvals, ticktext } = remapTickLabels({
        h_axis_data: xValues,
        labels: labels
    });

    Plotly.relayout({{ data.uid }}_element, {
        'xaxis.tickvals': tickvals,
        'xaxis.ticktext': ticktext,
        'xaxis.tickmode': 'array'
    });
});


