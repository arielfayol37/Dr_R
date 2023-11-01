

addEventListener('DOMContentLoaded', () => {

    const ExtraFunctionDiv = document.querySelector('.extra-functions');
    const list = document.querySelectorAll('.selected-students');
    const selected_action = document.querySelector('.selected-action');
    const button_action = document.querySelector('.action-button');

    // for extend due date function
    const selected_assignments = document.querySelector('.selected-assignments');
    const DueDateDiv = document.querySelector('.due-date-div');
    //add elements of other actions here
    //


    document.addEventListener('click', (event) => {

        if (event.target.classList.contains('select-button')) { // button to start selecting students and perform action
            checkboxes = document.querySelectorAll('.td-checkbox');
            selectBtn = event.target;
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

    // To sELECT AND display a particular action, and it's associate elements.

    selected_action.addEventListener('click', (event) => {
        DueDateDiv.style.display = 'none';

        if (selected_action.value === 'action-1') {
            DueDateDiv.style.display = 'inline';
            save_btn= DueDateDiv.querySelector('.save-new-due-date-field')
                save_btn.addEventListener('click',()=>{
                    console.log('kfj')
                    try {
                        list.forEach((student) => {
                            console.log('kfjdlk')
                            if (student.checked) { extend_due_date(selected_assignments.value, student.value); }
                        })
                        alert('Done');

                    }
                    catch { alert('Something went wrong'); }
                })

        }

        // add actions here
        //

    })

    /***************************************** FUNCTIONS OF DIFFERENT ACTIONS******************************/

    function extend_due_date(assignmentid, student_id) {

        new_date_field = DueDateDiv.querySelector('input[class=input-new-due-date-field]');
        // rearranging the url before fetching
        url = window.location.href;
        Url = '';
        for (o = 0; o < url.length - '/gradebook'.length; o++) {
            Url = Url + url[o]
        }
        //fecthing
             fetch(Url + '/' + student_id + '/student_profile/' + assignmentid + '/'
            + encodeURIComponent(new_date_field.value) +'/edit_student_assignment_due_date')
            .then(response => response.json())
            .then(result => {
                if (result.error) {
                    alert(result.error)
                }
                else {
                    if (!result.success) {
                        alert(result.message);
                    }
                }
            })
            .catch(error => console.error('Error', error));
    }

    //Add functions here
    //

}) 