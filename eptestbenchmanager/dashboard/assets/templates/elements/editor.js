var {{ data.uid }}_socket = io('{{ data.namespace }}');
ace.config.set("basePath", "/static/ace");
const editor = ace.edit("{{ data.uid }}_editor");
            editor.setTheme("ace/theme/monokai");
            editor.session.setMode("ace/mode/yaml");

function save(){
    const content = editor.getValue();
    const file_root = document.getElementById("{{ data.uid }}_file_root").value;
    const data = {
        'content': content,
        'file_root': file_root

    };
    {{ data.uid }}_socket.emit('save', data);
}

document.addEventListener('keydown', function(event) {
    if ((event.ctrlKey || event.metaKey) && event.key === 's') {
        event.preventDefault();
        save();
    }
});

{{ data.uid }}_socket.on('save_status', function(data){
    if (data.status === 'success'){
        alert('Saved successfully');
    }
    else{
        alert('Error saving');
    }

    if('redirect' in data){
        const url = new URL(window.location.href);
        url.pathname = url.pathname.replace(/\/[^/]+$/, "/"+data.redirect);
        window.location.href = url.href;
    }
}
);

function adjustInputWidth() {
  const input = document.getElementById('{{ data.uid }}_file_root');
  const mirror = document.getElementById('{{ data.uid}}_editor_name_mirror');
  
  // Update the mirror's text content with the input's value.
  // Append a non-breaking space to avoid zero width when input is empty.
  mirror.textContent = input.value || '\u00A0';
  
  // Get the computed width of the mirror element.
  const mirrorWidth = mirror.getBoundingClientRect().width;
  
  // Set a little extra space (e.g., 5px) for the caret.
  input.style.width = mirrorWidth + 5 + 'px';
}

// Adjust width on page load
adjustInputWidth();

// Adjust width as user types
document.getElementById('{{ data.uid }}_file_root').addEventListener('input', adjustInputWidth);

