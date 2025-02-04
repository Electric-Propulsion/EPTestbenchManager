var {{ data.uid }}_socket = io('{{ data.namespace }}');
function set_apparatus(  ) {
    var apparatus_uid = document.getElementById("{{ data.uid }}_apparatus_selector").value;
    {{ data.uid }}_socket.emit('set_apparatus', {'apparatus': apparatus_uid});
    }