
    text= document.querySelector('textarea');
    text.value='';
    a_tag= "document.querySelector('#save_link')";
    button_data='';
    document.querySelector('#edit-section').addEventListener('click',(event)=>{
        
        parent_= event.target.parentNode;
        if(parent_.classList.contains('col-sm-3')){

            button_data = event.target.dataset.categorie
            text.value= event.target.dataset.info;
            original_content=text.value;
            document.querySelector('input[name=categorie]').value= button_data;
            text.scrollIntoView({behaviour:'smooth'});
            text.style.height='500px';
           
        }
    })

    document.querySelector('input[value=Cancel]').addEventListener('click',(event)=>{
        event.preventDefault();
        text.value=original_content;
        a_tag.href= "#"
        
    })

    // document.querySelector('input[name=categorie]').addEventListener('click',(event)=>{
    //     event.preventDefault();
    //     if(button_data === ''){
    //         a_tag.href= "#";
    //     }
    //     else{
    //         a_tag.href= button_data + '/'+ text.value +'/save_course_info'; // useless  code
    //     csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]')
    //     fetch( button_data +'/save_course_info',{
    //         method: "POST",
    //         body: JSON.stringify({
    //             "title": "foo",
    //             "body": "bar",
    //             "userId": 1
    //         }),
    //         credentials: 'same-origin',
    //         headers: {"X-CSRFToken": csrf_token.value,
    //         "Content-type": "application/json; charset=UTF-8"}
    //     }).then(response=>response.json())
    //     .then(result=>{
    //         if(result){
    //             window.location.replace(window.location.href);
    //         }
    //     })
    //     }
    // })

    document.querySelector('button[id=Edit]').addEventListener('click',(event)=>{
        edit_section =document.querySelector('#edit-section')
        edit_section.style.display='block';
        edit_section.scrollIntoView({behaviour:'smooth'})
    })


