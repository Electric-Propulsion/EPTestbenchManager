var {{ data.uid }}_socket = io('{{ data.namespace }}');
{{ data.uid }}_socket.on('reload', function(data) {
    location.reload();
});