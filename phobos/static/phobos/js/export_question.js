
  document.addEventListener('DOMContentLoaded', ()=>{

    export_question= document.querySelector('.export_question')
    btn_export_question = export_question.querySelector('button')
    export_to_assignment = export_question.querySelector('div')
    export_result= export_question.querySelector('.export_result')
    select_assignment='';
    selected_course_id='';
    select_course=export_to_assignment.querySelector('select[id=select_course]');


    document.querySelector('#btn-export_question').addEventListener('click',()=>{  
        export_to_assignment.style.display='block';
        export_result.style.display= 'none';
        export_to_assignment.querySelector('input[type=button]').value='Select Course';
    })

    export_to_assignment.querySelector('input[type=button]').addEventListener('click',(event)=>{ 

             if(event.target.classList.contains('export-confirm') && selected_course_id !='' ){   // excute back_end export function and return result
                select_assignment= export_to_assignment.querySelector('#' + selected_course_id)
                fetch(window.location.href+ '/export_question_to/'+ select_assignment.value) 
                .then(response=>response.json())
                .then(result=>{
                    alert(result);
                    export_result.style.display= 'block';
                    export_to_assignment.style.display='none';
                    select_assignment.style.display= 'none';
            })}
            else{  //display a particular lists of assignment for the selected course
                selected_course_id=  export_to_assignment.querySelector('select[id=select_course]').value
                select_assignment= export_to_assignment.querySelector('#' + selected_course_id)
                select_assignment.style.display= 'inline';
                export_to_assignment.querySelector('input[type=button]').value='Confirm';
            }
        
    })
                // display a particular lists of assignment if the selected course is changed
    select_course.addEventListener('change',()=>{
        select_assignment.style.display= 'none';
                selected_course_id=  export_to_assignment.querySelector('select[id=select_course]').value;
                // console.log('#' + selected_course_id)
                select_assignment= export_to_assignment.querySelector('#' + selected_course_id)
                select_assignment.style.display= 'inline';
                export_to_assignment.querySelector('input[type=button]').value='Confirm';

    })


  })
