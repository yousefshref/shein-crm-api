window.addEventListener('load', function() {
    // Optionally, add a slight delay if necessary
    setTimeout(function() {
        // Look for all inline groups; adjust this selector if needed
        var inlineGroups = document.querySelectorAll('.inline-group');
        inlineGroups.forEach(function(group) {
            var addRow = group.querySelector('.add-row');
            if (addRow) {
                // Move the add-row element to the top of the inline group
                group.insertBefore(addRow, group.firstChild);
            }
        });
    }, 500); // 500ms delay; adjust as necessary
});
