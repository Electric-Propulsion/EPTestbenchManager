var {{ data.uid }}_socket = io('{{ data.namespace }}');
{{ data.uid }}_socket.on('update', function(data) {
    document.getElementById('{{ data.uid }}').getElementsByClassName('dg_value_entry')[0].value = data.value;
});

{{ data.uid }}_entry_element = document.getElementById('{{ data.uid }}_value_entry');

// Prevent clicks on the "no-link" element from following the parent <a> link
{{ data.uid }}_entry_element.addEventListener('click', function(event) {
    event.stopPropagation(); // Prevents the event from bubbling up to the <a>
    event.preventDefault(); // Prevents the default link action
});

// Prevent clicks on the "no-link" element from following the parent <a> link
{{ data.uid }}_entry_element.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.stopPropagation(); // Prevents the keydown event from bubbling up
            event.preventDefault(); // Prevents the default "link activation" action
            // Handle Enter key behavior if necessary (e.g., submit or process the value)
            {{ data.uid }}_socket.emit('set_value', { value: event.target.value });
            {{ data.uid }}_entry_element.classList.remove('unsaved');
        }
    });

// Add input event listener to detect when the value changes
{{ data.uid }}_entry_element.addEventListener('input', function() {
    // Add the "unsaved" class to indicate the value has changed
    {{ data.uid }}_entry_element.classList.add('unsaved');
});

// Add blur event listener to handle the user clicking away
{{ data.uid }}_entry_element.addEventListener('blur', function() {
    // If the input has been changed (unsaved), keep the "unsaved" class
    if ({{ data.uid }}_entry_element.value !== '' && {{ data.uid }}_entry_element.classList.contains('unsaved')) {
        {{ data.uid }}_entry_element.classList.add('unsaved'); // Keep the red state
    }
});



