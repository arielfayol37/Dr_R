

document.addEventListener('DOMContentLoaded', () => {

    const ExtraFunctionDiv = document.querySelector('.extra-functions');
    const list = document.querySelectorAll('.selected-students');
    const selected_action = document.querySelector('.selected-action');
    const button_action = document.querySelector('.action-button');

    //adding an event dispatcher
    const selectBtn = document.querySelector('.select-button');

    // for extend due date function
    const selected_assignments = document.querySelector('.selected-assignments');
    const DueDateDiv = document.querySelector('.due-date-div');

    const checkboxes = document.querySelectorAll('.td-checkbox');
    //add elements of other actions here
    document.addEventListener('click', (event) => {

        if (event.target == selectBtn) { // button to start selecting students and perform action
            if (selectBtn.innerHTML === 'Select Students') {
                button_action.style.display = 'inline';
                ExtraFunctionDiv.style.display = 'inline';
                selectBtn.innerHTML = 'Cancel';
                checkboxes.forEach((checkbox) => { checkbox.style.display = 'inline'; })
            }
            else {
                ExtraFunctionDiv.style.display = 'none'; // hiding checkboxes
                selectBtn.innerHTML = 'Select Students';
                checkboxes.forEach((checkbox) => { checkbox.style.display = 'none'; })
            }
        }

        if (event.target.classList.contains("action-button")) { // display action list
            selected_action.style.display = 'inline';
        }

        if (event.target.classList.contains('select-all-students')) { // Checkbok to select all students at once
            if (event.target.checked) {
                list.forEach((student) => { student.checked = true })
            }
            else {
                list.forEach((student) => { student.checked = false })
            }
        }
    })

    const save_btn= DueDateDiv.querySelector('.save-new-due-date-field');
    save_btn.addEventListener('click',()=>{
        try {
            let selectedPksArray = []
            list.forEach((student) => {
                if (student.checked) {
                selectedPksArray.push(student.value);   
                } 
            });
            console.log(selectedPksArray);
            if(selectedPksArray.length != 0){
                extend_due_date(selected_assignments.value, selectedPksArray);
                ExtraFunctionDiv.style.display = 'none'; // hiding checkboxes
                selectBtn.innerHTML = 'Select Students';
                checkboxes.forEach((checkbox) => { checkbox.style.display = 'none'; })
            } else{
                alert('You did not select any student');
                return;
            }
        }
        catch (error) { // Make sure to capture the error object
            console.error('Something went wrong:', error);
            // If you still want to alert the user, keep the alert line, otherwise remove it.
            alert('Something went wrong');
        }
    })
    // To sELECT AND display a particular action, and it's associate elements.

    selected_action.addEventListener('click', (event) => {
        event.preventDefault();
        DueDateDiv.style.display = 'none';

        if (selected_action.value === 'action-1') {
            DueDateDiv.style.display = 'inline';

        }

        // add actions here
        //

    })

    /***************************************** FUNCTIONS OF DIFFERENT ACTIONS******************************/

    function extend_due_date(assignmentid, selected_pks) {
        const new_date_field = DueDateDiv.querySelector('.input-new-due-date-field');
        
        const baseUrl = window.location.href.replace('/gradebook', '');
        
        // Fetching
        fetch(`${baseUrl}/student_profile/${assignmentid}/edit_student_assignment_due_date`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                new_date: new_date_field.value,
                selected_ids: selected_pks
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
            return response.json();
        })
        .then(result => {
            if (result.success) {
                // Handle success
                console.log('Due date extended successfully.');
            } else {
                // Handle failure
                alert(result.message || 'An error occurred while extending the due date.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred: ' + error.message);
        });
    }
    

    function getCookie(name) {
        if (!document.cookie) {
          return null;
        }
    
        const csrfCookie = document.cookie
          .split(';')
          .map(c => c.trim())
          .find(c => c.startsWith(name + '='));
    
        if (!csrfCookie) {
          return null;
        }
    
        return decodeURIComponent(csrfCookie.split('=')[1]);
      }

}) 