document.addEventListener("DOMContentLoaded", () => {
    // Initialize application
    assignmentDetailsInit();

    // Add global event listeners
    addGlobalEventListeners();

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


    // Function to initialize assignment details
    function assignmentDetailsInit() {
        const assignments = document.querySelectorAll('.assignment');
        assignments.forEach(assignment => {
            assignment.addEventListener('click', () => handleAssignmentClick(assignment));
        });
    }

    // Handle assignment click
    function handleAssignmentClick(assignment) {
        assignment.style.color = 'black';
        const assignmentId = parseInt(assignment.id);

        if (!document.querySelector(`#table${assignmentId}`)) {
            fetch(`get_questions/${encodeURIComponent(assignmentId)}`)
                .then(res => res.json())
                .then(question => tableGenerator(question, assignmentId))
                .catch(error => console.error('Error fetching questions:', error));
        }
    }

    // Function to add global event listeners
    function addGlobalEventListeners() {
        document.body.addEventListener('click', handleGlobalClick);
    }

    // Handle global click events
    function handleGlobalClick(event) {
        const target = event.target;

        handleDueDateExtension(target);
        handleScoreEdit(target);
        handleScoreEditToggle(target);
    }

// Handle due date extension
function handleDueDateExtension(target) {
    // Show due date extension input
    if (target.classList.contains('due_date-btn')) {
        const dueDateDiv = target.parentNode.querySelector('.due-date-div');
        dueDateDiv.style.display = 'inline';
        target.style.display = 'none';
    }

    // Save new due date
    if (target.classList.contains('save-new-due-date-field')) {
        const dueDateDiv = target.parentNode;
        const dueDateInput = dueDateDiv.querySelector('.input-new-due-date-field');
        const dueDateBtn = dueDateDiv.parentNode.querySelector('.due_date-btn');
        const assignmentId = dueDateBtn.dataset.assignmentid;
        const newDueDate = dueDateInput.value;

        if (newDueDate) {
            updateDueDate(assignmentId, newDueDate, dueDateDiv, dueDateBtn);
        }
    }
}

// Update the due date on the server
function updateDueDate(assignmentId, newDueDate, dueDateDiv, dueDateBtn) {
    // Implement the logic to send the new due date to the server
    fetch(`${window.location.href}/${assignmentId}/edit_student_assignment_due_date`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ new_date: newDueDate })
    })
    .then(response => response.json())
    .then(result => {
        alert(result.message);
        if (result.success) {
            const dueDateDisplay = dueDateDiv.parentNode.querySelector('.Due-date-display');
            dueDateDisplay.textContent = `Due by: ${newDueDate}`;
            dueDateDiv.style.display = 'none';
            dueDateBtn.style.display = 'inline';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to update due date.');
    });
}


// Handle score editing
function handleScoreEdit(target) {
    if (target.classList.contains('edit-score-line')) {
        const row = target.closest('tr');
        const scoreCell = row.querySelector('.score_record');
        const questionStudentId = target.dataset.questionStudentId;
        const originalScore = scoreCell.dataset.originalScore;
        const editSection = document.createElement('div');
        editSection.classList.add('edit-section');
        const editInput = document.createElement('input');
        editInput.type = 'number';
        
        editInput.classList.add('edit-score-input', 'field-style');

        editInput.value = scoreCell.querySelector('.value').textContent;
        const dSection = scoreCell.querySelector('.d-section');
        dSection.style.display = 'none';

        editSection.appendChild(editInput);
        //scoreCell.appendChild(editInput);

        const saveButton = document.createElement('button');
        saveButton.innerText = 'save';
        saveButton.classList.add('save-score-btn', 'btn', 'btn-outline-info');
        saveButton.onclick = () => saveEditedScore(questionStudentId, editInput.value, scoreCell);
        editSection.appendChild(saveButton);

        const oScoreSpan = document.createElement('span')
        oScoreSpan.innerHTML = ` Initial: ${originalScore}`;

        editSection.appendChild(oScoreSpan);

        //scoreCell.appendChild(saveButton);
        scoreCell.appendChild(editSection);
    }
}

// Save the edited score
function saveEditedScore(questionStudentId, newScore, scoreCell) {
    // Implement the logic to send the new score to the server
    // For example, using fetch to send a POST request
    fetch(`student_profile/modify_question_student_score/${newScore}/${questionStudentId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(result => {
        alert(result.message);
        if (result.success) {
            scoreCell.querySelector('.value').innerHTML = result.new_score;
            scoreCell.querySelector('.d-section').style.display = 'block';
            scoreCell.removeChild(scoreCell.querySelector('.edit-section'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to save score.');
    });
}


// Toggle score editing mode
function handleScoreEditToggle(target) {
    if (target.classList.contains('edit-score-btn')) {
        const table = target.closest('.generated_assignment_table');
        const editScoreLines = table.querySelectorAll('.edit-score-line');

        if (target.textContent === 'Edit Scores') {
            editScoreLines.forEach(line => {
                line.style.display = 'inline';
            });
            target.textContent = 'Cancel';
        } else {
            editScoreLines.forEach(line => {
                line.style.display = 'none';
            });
            target.textContent = 'Edit Scores';
        }
    }
}

// Generate assignment detail table
function tableGenerator(questions, assignmentId) {
    const container = document.querySelector('.body-container');
    const div = document.createElement('div');
    div.id = 'table' + assignmentId;
    div.className = 'generated_assignment_table';

    // Create title and controls
    div.appendChild(createTableTitle(questions[0], assignmentId));

    // Create table
    const table = document.createElement('table');
    table.className = 'table table-striped table-bordered table-hover';
    table.appendChild(createTableHeader(questions));
    table.appendChild(createTableBody(questions));

    div.appendChild(table);
    container.appendChild(div);
    div.scrollIntoView({ behavior: 'smooth' });
}

// Create table title and controls
function createTableTitle(question, assignmentId) {
    const titleDiv = document.createElement('div');
    titleDiv.innerHTML = `
        <h3>${question.name} details</h3>
        <span class='Due-date-display suggestion original-size'>Due by: ${question.Due_date}</span>
        <button class="btn btn-outline-info due_date-btn" data-assignmentId="${assignmentId}">Extend Due Date</button>
        <button class="btn btn-outline-success edit-score-btn">Edit Scores</button>
        <div class="due-date-div" style="display: none;">
            <input type="datetime-local" class="input-new-due-date-field">
            <input type="button" class="save-new-due-date-field btn btn-outline-success" value="Apply">
        </div>`;
    return titleDiv;
}

// Create table header
function createTableHeader(questions) {
    const thead = document.createElement('thead');
    const tr = document.createElement('tr');
    
    // Assuming the first question object has all necessary fields
    Object.keys(questions[1]).forEach(key => {
        if (key !== 'id' && key !== 'original_score' && key !== 'real_score' && key !== 'total') {
            const th = document.createElement('th');
            th.textContent = key;
            tr.appendChild(th);
        }
    });

    thead.appendChild(tr);
    return thead;
}

// Create table body
function createTableBody(questions) {
    const tbody = document.createElement('tbody');

    questions.slice(1).forEach(question => {
        const tr = document.createElement('tr');
        Object.entries(question).forEach(([key, value]) => {
            if (key !== 'id' && key !== 'original_score' && key !== 'real_score' && key !== 'total') {
                const td = document.createElement('td');
                if (key === 'score') {
                    td.dataset.originalScore = question.original_score;
                    td.className = 'score_record';
                    td.innerHTML = `<div class="d-section"><span class='score-record'><span class="value">${question.real_score}</span>/${question.total}</span>
                                    <u class='edit-score-line' data-question-student-id=${question.id} style="display: none;">edit</u></div>`;
                } else {
                    td.textContent = value;
                }
                tr.appendChild(td);
            }
        });
        tbody.appendChild(tr);
    });

    return tbody;
}

});
