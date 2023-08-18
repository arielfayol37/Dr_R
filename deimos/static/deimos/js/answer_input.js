document.addEventListener('DOMContentLoaded', ()=> {
    const answerFieldsDiv = document.querySelector('.answer-fields');
    const form = document.querySelector('#question-form');
    const validateAnswerActionURL = extractQuestionPath(window.location.href) + '/validate_answer';
    //console.log(newActionURL);
    //form.setAttribute('action', newActionURL);
    const submitBtn = document.querySelector('submit-btn');
    const formattedAnswerDiv = document.querySelector('.formatted-answer');
    const calculatorDiv = document.querySelector('.calculator');
    const inputedMcqAnswersDiv = document.querySelector('.inputed-mcq-answers');
    var num_true_counter = 0;
    const screen = document.querySelector('#screen'); 

/*-----------------------------Question submission-----------------------*/

    submitBtn.addEventListener('click', (event){
        event.preventDefault();
    })

/*----------------------------DISPLAYING LATEX-------------------------*/

function displayLatex(){
    const formattedAnswerDivs = document.querySelectorAll('.formatted-answer');
    MathJax.typesetPromise().then(() => {
        formattedAnswerDivs.forEach((formattedAnswerDiv) => {
            try {
                const inputElement = formattedAnswerDiv.querySelector('.latex-answer-question-view');
                if (inputElement != null){
                    const formatted_answer = MathJax.tex2chtml(inputElement.value + '\\phantom{}');
                    //inputElement.remove();
                    formattedAnswerDiv.appendChild(formatted_answer);
                    MathJax.typesetPromise();
                }

            } catch (error) {
                console.log(error);
            }
        });
    });

}

displayLatex();

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
                MathJax.typesetPromise();
                } catch (error) {
                   //console.log(error);
                }
                
                }); 
        
        })
        
    }


    form.addEventListener('submit', (event)=>{
        event.preventDefault();
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

function extractQuestionPath(url) {
    const startIndex = url.indexOf('courses');
    if (startIndex !== -1) {
        return url.substring(startIndex);
    } else {
        return null; // If 'courses' not found in URL
    }
}

});
