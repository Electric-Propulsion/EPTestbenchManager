var {{ data.uid }}_socket = io('{{ data.namespace }}');
function start_experiment(  ) {
    var experiment_uid = document.getElementById("{{ data.uid }}_experiment_selector").value;
    var operator = document.getElementById("{{ data.uid }}_operator_selector").value;
    {{ data.uid }}_socket.emit('start_experiment', {'experiment_uid': experiment_uid, 'operator': operator});
    }

function edit_experiment(  ) {
    var experiment_uid = document.getElementById("{{ data.uid }}_experiment_selector").value;
    window.location.href = '/{{ data.experiment_config_path }}/'+experiment_uid;
    }

function new_experiment(  ) {
    window.location.href = '/{{ data.experiment_config_path }}/untitled_experiment';
    }

function request_abort(  ) {
    {{ data.uid }}_socket.emit('request_abort');
    }