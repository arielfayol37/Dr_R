


function table_generator(question,assignment_id){
   
    div = document.createElement('div');
    div.id = 'table' + assignment_id;

    title = document.createElement('h3');
    title.innerHTML = question[0].name + " details";
    div.appendChild(title);

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
