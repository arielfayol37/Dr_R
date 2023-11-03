


function table_generator(question, assignment_id) {

    div = document.createElement('div');
    div.id = 'table' + assignment_id;
    div.className='generated_assignment_table';

    title = document.createElement('div');
    title.innerHTML = `</br><h3>${question[0].name} details </h3>
   <br/>
   <b class='Due-date-display'>Due by: ${question[0].Due_date} </b> <button class="btn edit-btn co due_date-btn"  data-assignmentId="${assignment_id}" style="display: inline; position:relative; float: right">Extend Due Date</button>
   
   <button class="btn edit-btn co edit-score-btn"  style="display: inline; position:relative; float: right">Edit Scores</button>

   <div  class="due-date-div" style="display: none; position:relative; float: right" >
       <input type="datetime-local"  class="input-new-due-date-field">
       <input type="button" class="save-new-due-date-field" value="OK">
       </div>
   </div>`;

    div.appendChild(title);

    // adding due date extend functionality


    table = document.createElement('table');
    table.className = "table table-striped table-bordered table-hover";

    thead = document.createElement('thead');
    tr = document.createElement('tr');
    var column = [];
    for (i = 1; i < question.length; i++) {
        for (var col in question[i]) {
            if (!column.includes(col) && col != 'id' && col != 'original_score') {
                column.push(col);
                th = document.createElement('th');
                th.innerHTML = col;
                tr.appendChild(th);
            }
        }
    }
    thead.appendChild(tr)
    table.appendChild(thead)

    tbody = document.createElement('tbody');
    for (i = 1; i < question.length; i++) {
        tr = document.createElement('tr');
        for (j = 0; j < column.length; j++) {
            td = document.createElement('td');

            // We place and edit button under elements of the score column
            field_heading = thead.querySelectorAll('th')[j];
            score_field_heading = thead.querySelectorAll('th')[1];
            questionNum_field_heading = thead.querySelectorAll('th')[0];

            if (field_heading.innerHTML === score_field_heading.innerHTML) {
                td.dataset.original_score = question[i]['original_score']
                td.className = 'score_record';
                td.innerHTML = `<span class='score-record'>${question[i][column[j]]} </span>
           <u  class='edit-score-line' data-question_student_id=${question[i]['id']} style="display: none;"> edit </u>`;
            }
            else {
                td.innerHTML = question[i][column[j]]
            }

            tr.appendChild(td);
        }
        tbody.appendChild(tr);
    }
    table.appendChild(tbody);

    div.appendChild(table);
    document.body.appendChild(div);
    div.scrollIntoView({behavior:'smooth'})

}


function assignment_details() {

    assignments = document.querySelectorAll('.assignment')
    for (i = 0; i < assignments.length; i++) {
        assignments[i].addEventListener('click', function () {
            this.style.color = 'black';
            let assignment_id = parseInt(this.id);

            //loading content and generating a particular assignment table if it wasn't done before
            if (document.querySelector('#table' + assignment_id) == null) {
                fetch(`get_questions/${encodeURIComponent(assignment_id)}`)
                    .then(res => res.json())
                    .then(question => table_generator(question, assignment_id))
            }
        })
    }
}

addEventListener("DOMContentLoaded", assignment_details)


// implementing due date extension function
document.body.addEventListener('click', (event) => {

    target = event.target;
    event.preventDefault();
    DueDateDiv = target.parentNode.querySelector('div[class=due-date-div]');
    if (target.classList.contains('due_date-btn')) {
        DueDateDiv.style.display = 'inline';
        dueDateBtn = target;
        target.style.display = 'none';
    }

    if (target.classList.contains('save-new-due-date-field')) {
        DueDateDiv = target.parentNode;
        dueDateBtn = target.parentNode.parentNode.querySelector('.due_date-btn');
        new_date_field = DueDateDiv.querySelector('input[class=input-new-due-date-field]');
        console.log(dueDateBtn.dataset.assignmentid)
        fetch(window.location.href + '/' + dueDateBtn.dataset.assignmentid + '/' + encodeURIComponent(new_date_field.value) + '/edit_student_assignment_due_date')
            .then(response => response.json())
            .then(result => {
                alert(result.message);
                if (result.success) {
                    dueDateBtn.style.display = 'inline';
                    target.parentNode.parentNode.querySelector('.Due-date-display').innerHTML = "Due by: " + new_date_field.value;
                    DueDateDiv.style.display = 'none';
                }
            })

    }
    // HANDLING MODIFY QUESTION SCORE ************
    if (target.classList.contains('edit-score-line')) {
        const EditQuestionDiv = document.querySelector('.edit_questions_details');
        const ApplyBtn = EditQuestionDiv.querySelector('.apply-btn');
        const CancelBtn = EditQuestionDiv.querySelector('.cancel-btn')
        const questionNum = EditQuestionDiv.querySelector('.question-num');
        const originalScore = EditQuestionDiv.querySelector('.original-score');
        const actualScore = EditQuestionDiv.querySelector('.actual-score');
        const newScoreInputField = EditQuestionDiv.querySelector('.new-score-input-field');
        const row = target.closest('tr');
        const cell = target.closest('td');
        const questionNumCell = row.firstElementChild;
        const question_student_id = target.dataset.question_student_id

        //positioning Edit question box
        position= event.target.closest('table').parentNode;
        console.log(position)
        EditQuestionDiv.parentNode.removeChild(EditQuestionDiv)
        position.parentNode.insertBefore(EditQuestionDiv,position)

        //initial Views
        EditQuestionDiv.style.display = 'block';
        EditQuestionDiv.scrollIntoView({behavior:'smooth'})
        actual_score = cell.querySelector('.score-record').innerHTML;
        actualScore.innerHTML = actual_score;
        questionNum.innerHTML = questionNumCell.innerHTML;
        originalScore.innerHTML = cell.dataset.original_score;

        //Events
        CancelBtn.addEventListener('click', () => {
            EditQuestionDiv.style.display = 'none';
        })
        ApplyBtn.addEventListener('click', () => {

            if (confirm('Are you sure you want to modify this score')) {
                new_score = newScoreInputField.value
                fetch(window.location.href + '/modify_question_student_score/' + new_score + '/' + question_student_id)
                    .then(response => response.json())
                    .then(result => {
                        alert(result.result)
                        if (result.success) {
                            cell.querySelector('.score-record').innerHTML = new_score;
                            EditQuestionDiv.style.display = 'none';
                        }
                    })
                    .catch(error => console.error('error', error))
            }

        })
    }

    if (target.classList.contains('edit-score-btn')) {
        const editScoreLines = document.querySelectorAll('.edit-score-line');
        const EditQuestionDiv = document.querySelector('.edit_questions_details');
        if (target.innerHTML != 'Cancel') {
            editScoreLines.forEach(line => {
                line.style.display = 'inline';
                line.style.color = 'blue';
            });
            target.innerHTML = 'Cancel';

        }
        else {
            editScoreLines.forEach(line => { line.style.display = 'none'; });
            target.innerHTML = 'Edit Scores';
            EditQuestionDiv.style.display = 'none';
        }
    }

})

