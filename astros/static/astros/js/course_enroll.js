document.addEventListener('DOMContentLoaded', ()=>{
    ul= document.querySelector('.course-list');
    ul.addEventListener('click',(event)=>{
        parent_ = event.target.parentNode;
        if(parent_.classList.contains('enrollment')){
            enrollment_div = parent_;
            btn_pre_Enroll = enrollment_div.querySelector('.pre-Enroll');
            code_input_field = enrollment_div.querySelector('input[type=number]');
            btn_valide_code = enrollment_div.querySelector('.validate-btn');
            code_input_field.style.display= 'block';
            btn_valide_code.style.display= 'block';
            btn_pre_Enroll.style.display='none';
            btn_valide_code.addEventListener('click',(event)=>{
                event.preventDefault();
                fetch('course_enroll/'+ btn_pre_Enroll.dataset.courseId +'/'+ code_input_field.value)
                .then(response=>response.json())
                .then(validation =>{
                    code_input_field.value='';
                    code_input_field.placeholder = validation.response;
                    if(validation.state){
                        window.location.href = validation.course_management_url;
                    }
                    else{
                        code_input_field.style.color='red';
                    }
                })
            })

        }
        
    });   
})