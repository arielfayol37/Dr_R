
    text= document.querySelector('textarea');
    text.value='';
    a_tag= document.querySelector('#save_link');
    button_data='';
    document.querySelector('#edit-section').addEventListener('click',(event)=>{
        event.preventDefault();
        parent_= event.target.parentNode;
        if(parent_.classList.contains('col-sm-3')){

            button_data = event.target.dataset.categorie
            text.value= event.target.dataset.info;
            original_content=text.value;
            
            text.scrollIntoView({behaviour:'smooth'});
            text.style.height='500px';
        }
    })

    document.querySelector('input[value=Cancel]').addEventListener('click',(event)=>{
        event.preventDefault();
        text.value=original_content;
        a_tag.href= "#"
        
    })

    document.querySelector('input[value=Save]').addEventListener('click',(event)=>{
        event.preventDefault();
        if(button_data === ''){
            a_tag.href= "#";
        }
        else{
            a_tag.href= button_data + '/'+ text.value +'/save_course_info';
        }
        
        window.location.replace(a_tag.href);
    })


