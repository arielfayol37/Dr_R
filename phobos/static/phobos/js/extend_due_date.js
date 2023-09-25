
document.addEventListener('DOMContentLoaded',()=>{
    
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
            fetch(window.location.href+'/'+ encodeURIComponent(new_date_field.value) +'/edit_assignment_due_date')
            .then(response=>response.json())
            .then(result=>{
                alert(result.message);
                if(result.success){ 
                    dueDateBtn.style.display='inline';
                    DueDateDiv.style.display='none';}
            })
        }
    })
    
    
})