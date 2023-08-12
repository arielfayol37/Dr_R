document.addEventListener('DOMContentLoaded', ()=> {
    const answerFieldsDiv = document.querySelector('.answer-fields');
    const form = document.querySelector('#question-form');
    let currentAction = form.getAttribute('action');
    const formattedAnswerDiv = document.querySelector('.formatted-answer');
    const calculatorDiv = document.querySelector('.calculator');
    const inputedMcqAnswersDiv = document.querySelector('.inputed-mcq-answers');
    var num_true_counter = 0;
    const screen = document.querySelector('#screen'); 

/*----------------------------DISPLAYING LATEX-------------------------*/

function displayLatex(){

    console.log('Trying to display latex.')
    const formattedAnswerDivs = document.querySelectorAll('.formatted-answer');
    MathJax.typesetPromise().then(() => {
        formattedAnswerDivs.forEach((formattedAnswerDiv) => {
            try {
                const inputElement = formattedAnswerDiv.querySelector('.latex-answer-question-view');
                if (inputElement != null){
                    const formatted_answer = MathJax.tex2chtml(inputElement.value + '\\phantom{}');
                    //inputElement.remove();
                    formattedAnswerDiv.appendChild(formatted_answer);
                }

            } catch (error) {
                console.log(error);
            }
        });
    });

}

setTimeout(displayLatex, 300);

    /*----------------------------MCQ QUESTION --------------------------------*/
    if (!(inputedMcqAnswersDiv === null)){
    inputedMcqAnswersDiv.addEventListener('click', (event)=>{
        event.preventDefault();
        target = event.target
        if(target.classList.contains('mcq-false')){
            target.classList.remove('mcq-false','btn-warning');
            target.classList.add('mcq-true', 'btn-info');
            target.innerHTML = 'True';
            num_true_counter += 1;
            const answer_info_input = target.parentNode.querySelector('.formatted-answer').querySelector('.answer_info');
            answer_info_input.value = rep(answer_info_input.value, 0, '1');
        } else if(target.classList.contains('mcq-true')){
            target.classList.add('mcq-false','btn-warning');
            target.classList.remove('mcq-true', 'btn-info');
            target.innerHTML = 'False'; 
            num_true_counter -= 1;    
            const answer_info_input = target.parentNode.querySelector('.formatted-answer').querySelector('.answer_info');
            answer_info_input.value = rep(answer_info_input.value, 0, '0');
        }
    })

    }

    if (!(screen === null)){

        screen.addEventListener('input', ()=> {
            MathJax.typesetPromise().then(() => {
                try {
        
                const userInputNode = math.parse(processString(screen.value));
                var userInputLatex = userInputNode.toTex();
                const formattedAnswer = MathJax.tex2chtml(userInputLatex + '\\phantom{}');
                formattedAnswerDiv.innerHTML = '';
                formattedAnswerDiv.appendChild(formattedAnswer);
                } catch (error) {
                   //console.log(error);
                }
                
                }); 
        
        })
        
    }


    form.addEventListener('submit', (event)=>{
        if (!(screen === null)){
        const userInputNode = math.parse(screen.value);
        var userInputString = userInputNode.toString();
        screen.value = userInputString;
        }
        if (!(inputedMcqAnswersDiv === null) && num_true_counter < 1){
            event.preventDefault();
            alert('Must select at least one MCQ answer as correct.');
        }
    });


    /*------------------------------UTILITY FUNCTIONS ----------------------------*/
function rep(str, index, char) {
    str = setCharAt(str,index,char);
    return str
}

function setCharAt(str,index,chr) {
    if(index > str.length-1) return str;
    return str.substring(0,index) + chr + str.substring(index+1);
}

});
