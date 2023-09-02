
function display(element){
    
}

function table_generator(question,assignment_id){
   
    div = document.createElement('div');
    div.id = 'table' + assignment_id;

    title = document.createElement('h3');
    title.innerHTML = question[0].name + " details";
    div.appendChild(title);
    title.style.display='inline';

    Display_button= document.createElement('button');
    Display_button.className='Hide_button';
    Display_button.style.display= 'inline';
    Display_button.value= true;
    Display_button.innerHTML='Hide';
    Display_button.addEventListener('click',function(){
        console.log(this.innerHTML);
        if(this.innerHTML === 'Hide'){
            this.innerHTML = '';
            console.log(this.innerHTML)
            let Parents = this.parentNode;
            Parents.style.display= 'none';
            document.querySelector('#' + assignment_id).style.color= 'blue';
        }
    })
    div.appendChild(Display_button);

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
    div.scrollIntoView(true);

}


function assignment_details(){
assignments = document.querySelectorAll('.assignment')

for(i=0;i<assignments.length;i++){ 
 
    assignments[i].addEventListener('click',function(){
        this.style.color='black';
        let assignment_id= parseInt(this.id);
        let div = document.querySelector('#table'+ assignment_id);
            //loading content and generating a particular assignment table if it wasn't done before
        if (document.querySelector('#table'+ assignment_id) == null) {
            fetch(`get_questions/${encodeURIComponent(assignment_id)}`)
                .then(res => res.json())
                .then(question => table_generator(question,assignment_id))
        }
        else if(div.querySelector('.Hide_button').innerHTML != 'Hide'){
            div.querySelector('.Hide_button').innerHTML = 'Hide';
            div.style.display='block';
        }
    
    })
}
}

addEventListener("DOMContentLoaded",assignment_details)

// add buttons to collapse tables
// add buttons and functions to display and collapse all tables