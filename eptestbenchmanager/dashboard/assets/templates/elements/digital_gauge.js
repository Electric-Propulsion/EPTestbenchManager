var {{ data.uid }}_socket = io('{{ data.namespace }}');
{{ data.uid }}_socket.on('update', function(data) {
    document.getElementById('{{ data.uid }}').getElementsByClassName('dg_value')[0].innerText = data.value;
});