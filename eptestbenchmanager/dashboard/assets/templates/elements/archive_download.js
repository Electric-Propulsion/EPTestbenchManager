var {{ data.uid }}_socket = io('{{ data.namespace }}');
function download_archive(  ) {
    var archive = document.getElementById("{{ data.uid }}_archive_selector").value;
    window.open('/archive/'+archive+'.zip', '_blank').focus();
    }