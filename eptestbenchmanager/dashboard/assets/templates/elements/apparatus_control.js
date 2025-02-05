var {{ data.uid }}_socket = io('{{ data.namespace }}');
function set_apparatus(  ) {
    var apparatus_uid = document.getElementById("{{ data.uid }}_apparatus_selector").value;
    {{ data.uid }}_socket.emit('set_apparatus', {'apparatus': apparatus_uid});
    }

function edit_apparatus(  ) {
    var apparatus_uid = document.getElementById("{{ data.uid }}_apparatus_selector").value;
    window.location.href = '/{{ data.apparatus_config_path }}/'+apparatus_uid+'.yaml';
    }

function new_apparatus(  ) {
    window.location.href = '/{{ data.apparatus_config_path }}/untitled_space_craft.yaml';
    }