document.addEventListener('DOMContentLoaded',()=>{
    // Get the form and search field elements
    const form = document.getElementById('search-form');
    const searchField = document.getElementById('search-field');

    if(searchField != null){
            // Add an event listener to the search field for the 'keydown' event
    searchField.addEventListener('keydown', function(event) {
        // Check if the pressed key is Enter (key code 13)
        if (event.key === 'Enter') {
            // Prevent the default form submission
            event.preventDefault();

            // Submit the form programmatically
            form.submit();
        }
    });
    searchField.addEventListener('input', function() {
        if(!searchField.classList.contains('active')){
            searchField.classList.add('active');
        }
        if(searchField.value.length === 0){
            searchField.classList.remove('active')
        }
        searchField.style.height = 'auto'; // Reset the height to auto
        searchField.style.height = (searchField.scrollHeight) + 'px'; // Set the height to match the content
    });
    searchField.dispatchEvent(new Event('input'));
        
    }
})