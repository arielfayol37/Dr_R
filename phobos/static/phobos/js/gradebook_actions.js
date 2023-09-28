

addEventListener('DOMContentLoaded',()=>{
state=true;

const list=document.querySelectorAll('.selected-students');
const selected_action= document.querySelector('.selected-action');
const button_action= document.querySelector('.action-button');
const selected_assignments= document.querySelector('.selected-assignments');
const DueDateDiv = document.querySelector('.due-date-div');
const ExtraFunctionDiv = document.querySelector('.extra-functions');

document.addEventListener('click',()=>{

    if(event.target.classList.contains("action-button")){ //Use to display action list
        selected_action.style.display= 'inline'; 
    }

    if(event.target.classList.contains('save-new-due-date-field')){ // For extend due date action.

        for(i=0; i < list.length; i++)
        {
            if(list[i].checked){extend_due_date(selected_assignments.value,list[i].value);}
        }
        if(state){
            alert('Done');
        }
        else{
            alert('Something went wrong');
        }
    }
    

    if(event.target.classList.contains('select-all-students')){ // Checkbok to select all students at once

        if(event.target.checked){
        for(i=0; i< list.length; i++){
            list[i].checked=true;
        }} 

        else{
        for(i=0; i< list.length; i++){
            list[i].checked=false;
        }}

    }

    if(event.target.classList.contains('select-button')){ // button to start selecting students and perform action
        td_list=document.querySelectorAll('.td-checkbox'); 
        if(event.target.innerHTML==='Select Students'){
            button_action.style.display='inline';
            ExtraFunctionDiv.style.display='inline';
            event.target.innerHTML='Cancel';

        for(i=0; i< td_list.length; i++){ // displaying checkboxes
            td_list[i].style.display='inline';
        }}

        else{
            ExtraFunctionDiv.style.display='none'; // hiding checkboxes
            event.target.innerHTML='Select Students';

        for(i=0; i< td_list.length; i++){
            td_list[i].style.display='none';
        }}
    }
})


selected_action.addEventListener('click',()=>{ // To display elements associated to a particular action.
DueDateDiv.style.display='none';

if(event.target.value==='action-1'){  
    DueDateDiv.style.display='inline';
}
})



function extend_due_date(assignmentid,student_id){

        new_date_field = DueDateDiv.querySelector('input[class=input-new-due-date-field]');
        // rearranging the url before fetching
        url= window.location.href;
        Url='';
        for (o=0; o<url.length -'/gradebook'.length; o++ ){
            Url= Url+ url[o]
        }
        //fecthing
        fetch( Url+'/'+student_id+'/student_profile/'+assignmentid+'/'+encodeURIComponent(new_date_field.value) +'/edit_student_assignment_due_date')
        .then(response=>response.json())
        .then(result=>{
            if(!result.success){
            alert(result.message);
        }
        console.log(result.success)

        })
// return false if something went wrong
    }
})