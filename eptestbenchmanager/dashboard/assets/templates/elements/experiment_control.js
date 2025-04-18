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

document.getElementById("{{ data.uid }}_experiment_selector").addEventListener('change', function() {
    var experiment_selector = document.getElementById("{{ data.uid }}_experiment_selector");
    var start_button = document.getElementById("{{ data.uid }}_start_button");
    var selected_option = experiment_selector.options[experiment_selector.selectedIndex];
    
    if (selected_option.classList.contains('disabled')) {
        start_button.disabled = true;
    } else {
        start_button.disabled = false;
    }
});
