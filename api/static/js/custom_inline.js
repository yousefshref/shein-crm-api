(function($) {
    // Listen for clicks on the "Add another Customer" button.
    $(document).on('click', '.add-row a', function(e) {
        // Wait for the new inline form to be added.
        setTimeout(function() {
            // Find the container for the Customer inline forms.
            // Adjust the selector to target your inline container. Often it has a class like 'inline-group'
            var container = $('.inline-group'); 
            
            // Identify the newly added form.
            // This code assumes the new inline is appended as the last '.form-row'
            var newForm = container.find('.form-row').last();
            
            // Prepend the new form to the container so it appears at the top.
            newForm.prependTo(container);
        }, 50); // A slight delay ensures the form is fully added.
    });
})(django.jQuery);
