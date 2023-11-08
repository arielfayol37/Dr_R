document.addEventListener('DOMContentLoaded', ()=>{
    const searchField = document.querySelector('.page-search');
    const itemsSearch = document.querySelectorAll(`.${searchField.dataset.name}`); // expecting the page to have items with classes
    var parentDivName = searchField.dataset.parent;
    var displayProperty = searchField.dataset.display;
    if(parentDivName == null){
        parentDivName = 'course-li'; // most pages will have course-li 
    }
    if(displayProperty == null){
        displayProperty = 'block';
    }                                                                            // corresponding to searchField.dataset.name 
    if(searchField != null){
        // Add an event listener to the search field for the 'keydown' event
        searchField.addEventListener('keydown', function(event) {
            // Check if the pressed key is Enter (key code 13)
            if (event.key === 'Enter') {
                // Prevent the default form submission
                event.preventDefault();
                itemsSearch.forEach((item)=>{
                    const itemString = item.textContent.toLocaleLowerCase();
                    // console.log(itemString);
                    if(itemString.includes(searchField.value.toLowerCase())){
                        item.closest(`.${parentDivName}`).style.display = displayProperty;
                    }else {
                        item.closest(`.${parentDivName}`).style.display = 'none';
                    }
                })

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