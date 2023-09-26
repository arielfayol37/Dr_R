


function table_generator(question,assignment_id){
   
   div = document.createElement('div');
   div.id = 'table' + assignment_id;

   title = document.createElement('div');
   title.innerHTML = `<h3>${question[0].name} details </h3>
   <br/>
   <b class='Due-date-display'>Due by: ${question[0].Due_date} </b> <button class="btn edit-btn co due_date-btn"  data-assignmentId="${assignment_id}" style="display: inline; position:relative; float: right">Extend Due Date</button>
   <div  class="due-date-div" style="display: none; position:relative; float: right" >
       <input type="date"  class="input-new-due-date-field">
       <input type="button" class="save-new-due-date-field" value="OK">
       </div>
   </div>`;
   div.appendChild(title);

   // adding due date extend functionality


   table = document.createElement('table');
   table.className = "table table-striped table-bordered table-hover";

   thead = document.createElement('thead');
   tr = document.createElement('tr');
   var column=[];
   for(i =1;i<question.length; i++){
       for(var col in question[i]){
           if(!column.includes(col)){
               column.push(col);
               td = document.createElement('th');
               td.innerHTML = col;
               tr.appendChild(td);
           }
       }
   }
   thead.appendChild(tr)
   table.appendChild(thead)

   tbody = document.createElement('tbody');
   for (i = 1; i < question.length; i++) {
       tr = document.createElement('tr');
       for(j=0; j< column.length; j++){
           td = document.createElement('td');
           td.innerHTML = question[i][column[j]];
           tr.appendChild(td);
       }
       tbody.appendChild(tr);
   }
   table.appendChild(tbody);

   div.appendChild(table);
   document.body.appendChild(div);

}


function assignment_details(){
assignments = document.querySelectorAll('.assignment')

for(i=0;i<assignments.length;i++){ 

   assignments[i].addEventListener('click',function(){
       this.style.color='black';
       let assignment_id= parseInt(this.id) ;

           //loading content and generating a particular assignment table if it wasn't done before
       if (document.querySelector('#table'+ assignment_id) == null) {
           fetch(`get_questions/${encodeURIComponent(assignment_id)}`)
               .then(res => res.json())
               .then(question => table_generator(question,assignment_id))
       }
   
   })
}
}

addEventListener("DOMContentLoaded",assignment_details)

// implementing due date extension function
    document.body.addEventListener('click',(event)=>{
        target= event.target;
        DueDateDiv = target.parentNode.querySelector('div[class=due-date-div]');
        if(target.classList.contains('due_date-btn')){
            DueDateDiv.style.display='inline'; 
            dueDateBtn=target;
            target.style.display='none'; 
        }
        
        if(target.classList.contains('save-new-due-date-field')){
            DueDateDiv = target.parentNode;
            dueDateBtn = target.parentNode.parentNode.querySelector('.due_date-btn');
            new_date_field = DueDateDiv.querySelector('input[class=input-new-due-date-field]');
            console.log(dueDateBtn.dataset.assignmentid)
            fetch( window.location.href+'/'+dueDateBtn.dataset.assignmentid+'/'+encodeURIComponent(new_date_field.value) +'/edit_student_assignment_due_date')
            .then(response=>response.json())
            .then(result=>{
                alert(result.message);
                if(result.success){ 
                    dueDateBtn.style.display='inline';
                    target.parentNode.parentNode.querySelector('.Due-date-display').innerHTML= "Due by: "+ new_date_field.value;
                    DueDateDiv.style.display='none';}
            })
        }
    })

