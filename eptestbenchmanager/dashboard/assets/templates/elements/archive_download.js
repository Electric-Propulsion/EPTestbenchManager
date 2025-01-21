var {{ data.uid }}_socket = io('{{ data.namespace }}');
function download_archive(  ) {
    var archive = document.getElementById("{{ data.uid }}_archive_selector").value;
    window.open('/archive/'+archive+'.zip', '_blank').focus();
    }
{{ data.uid }}_socket.on('update', function(data) {
    var archive_selector = document.getElementById("{{ data.uid }}_archive_selector");
    Array.from(archive_selector.options).forEach(function(option) {
        archive_selector.remove(option);
    });
    data.archives.forEach(function(archive) {
        var option = document.createElement("option");
        option.text = archive;
        archive_selector.add(option);
    });
});