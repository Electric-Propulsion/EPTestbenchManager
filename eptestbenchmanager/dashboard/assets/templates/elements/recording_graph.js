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

// Function to format relative time for rolling graphs
function formatRelativeTimeDynamic(timestamp) {
    const now = Date.now(); // Client-side current time in ms
    const delta = now - timestamp * 1000; // Convert server timestamp to ms
    const deltaInSeconds = Math.floor(delta / 1000);

    const days = Math.floor(deltaInSeconds / (24 * 3600));
    const hours = Math.floor((deltaInSeconds % (24 * 3600)) / 3600);
    const minutes = Math.floor((deltaInSeconds % 3600) / 60);
    const seconds = deltaInSeconds % 60;
    const millis = Math.floor(delta % 1000); // Truncate to three digits

    if (deltaInSeconds < 0) {
        // Cap at T-0:00
        return "T-0:00.000";
    }

    if (days > 0) {
        return `T-${days} days, ${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}.${String(millis).padStart(3, '0')}`;
    } else {
        return `T-${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}.${String(millis).padStart(3, '0')}`;
    }
}

// Function to format absolute time for non-rolling graphs
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

// Generate labels based on mode (rolling or absolute)
function generateLabel(timestamp) {
    if ('{{ data.rolling }}' === 'True') {
        return formatRelativeTimeDynamic(timestamp);
    } else {
        return formatAbsoluteTime(timestamp);
    }
}

// Update rolling labels for all points
function updateRollingLabels(data) {
    return data.h_axis_data.map((timestamp) => formatRelativeTimeDynamic(timestamp));
}

// Socket event: Update graph with new data
{{ data.uid }}_socket.on('update', function(data) {
    if ('{{ data.rolling }}' === 'True') {
        {{ data.uid }}_data[0].x = data.h_axis_data;
        {{ data.uid }}_data[0].y = data.v_axis_data;
        {{ data.uid }}_data[0].text = updateRollingLabels(data);
    } else {
        {{ data.uid }}_data[0].x = data.h_axis_data;
        {{ data.uid }}_data[0].y = data.v_axis_data;
        {{ data.uid }}_data[0].text = data.h_axis_data.map(generateLabel);
    }

    const { tickvals, ticktext } = remapTickLabels(data);
    {{ data.uid }}_layout.xaxis.tickvals = tickvals;
    {{ data.uid }}_layout.xaxis.ticktext = ticktext;
    {{ data.uid }}_layout.xaxis.tickmode = 'array';

    Plotly.react({{ data.uid }}_element, {{ data.uid }}_data, {{ data.uid }}_layout);
});

// Socket event: Append a single point to the graph
{{ data.uid }}_socket.on('append_point', function(data) {
    const newTimestamp = data.h_axis_datapoint;
    const newValue = data.v_axis_datapoint;

    const newPoint = {
        x: [[newTimestamp]],
        y: [[newValue]],
        text: [[generateLabel(newTimestamp)]]
    };

    if ('{{ data.rolling }}' === 'True') {
        Plotly.extendTraces({{ data.uid }}_element, newPoint, [0], {{ data.max_points }});
        const updatedLabels = {{ data.uid }}_data[0].x.map((timestamp) =>
            formatRelativeTimeDynamic(timestamp)
        );
        {{ data.uid }}_data[0].text = updatedLabels;
    } else {
        Plotly.extendTraces({{ data.uid }}_element, newPoint, [0]);
    }

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

// Function to update rolling labels dynamically at regular intervals
function updateRollingGraphLabelsPeriodically(interval) {
    if ('{{ data.rolling }}' === 'True') {
        setInterval(() => {
            // Update the labels for all points in the rolling graph
            const updatedLabels = {{ data.uid }}_data[0].x.map((timestamp) =>
                formatRelativeTimeDynamic(timestamp)
            );
            {{ data.uid }}_data[0].text = updatedLabels;

            // Reapply tick labels and tick values
            const { tickvals, ticktext } = remapTickLabels({
                h_axis_data: {{ data.uid }}_data[0].x,
                labels: updatedLabels
            });

            Plotly.relayout({{ data.uid }}_element, {
                'xaxis.tickvals': tickvals,
                'xaxis.ticktext': ticktext,
                'xaxis.tickmode': 'array'
            });
        }, interval);
    }
}

// Call the function to start periodic updates (e.g., every 1 second)
updateRollingGraphLabelsPeriodically(1000);
