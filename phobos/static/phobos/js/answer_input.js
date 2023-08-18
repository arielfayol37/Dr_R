
document.addEventListener('DOMContentLoaded', () => {

    const expressionBtn = document.querySelector('#expression-btn');
    const answerFieldsDiv = document.querySelector('.answer-fields');
    const mcqAnswersDiv = document.querySelector('.mcq-answers');
    const form = document.querySelector('#question-form');
    let currentAction = form.getAttribute('action');
    const mcqBtn = document.querySelector('#mcq-btn');
    const mcqOptionBtnsDiv = mcqAnswersDiv.querySelector('.mcq-options-button');
    const inputedMcqAnswersDiv = document.querySelector('.inputed-mcq-answers');
    var num_mcq_options_counter = 2;
    var num_true_counter = 0;
    var option_counter = 0;

    const addMcqOptionBtn = document.querySelector('.mcq-add');
    
    const mcqInputDiv = document.querySelector('.mcq-input-div');
    const mcqInputField = mcqInputDiv.querySelector('.mcq-input-field');
    const floatBtn = document.querySelector('#float-btn');
    const latexBtn = document.querySelector('#latex-btn');
    const frBtn = document.querySelector('#fr-btn');
    const surveyBtn = document.querySelector('#survey-btn');
    latexBtn.style.display = 'none';
    const formattedAnswerDiv = document.querySelector('#structural-formatted-answer');
    const screen = document.querySelector('#screen'); 
    const calculatorDiv = document.querySelector('.calculator');
    calculatorDiv.style.display = 'none';
    let mode = '';

 /*------------------------------------------MCQ QUESTION --------------------------------- */
 



    mcqBtn.addEventListener('click', (event)=>{
    
    event.preventDefault();
        inputedMcqAnswersDiv.style.display = 'block';
        mode = 'm-answer'
        num_mcq_options_counter = 0; // TODO: change this in case you want store the already inputed mcqs when the user 
                                    // changes answer type options. For example he may click on expression then come back to mcq.
        formattedAnswerDiv.style.display = 'none';
        calculatorDiv.style.display = 'none';
        mcqOptionBtnsDiv.style.display = 'block';
        // Append '/3' at the end of the URL
        const newAction = currentAction + '/3';
        // Update the form's action attribute
        form.setAttribute('action', newAction);
        

    });
    
    mcqOptionBtnsDiv.addEventListener('click', (event)=> {
        event.preventDefault();
        mcqInputDiv.style.display = 'block';
        switch (event.target.id) {
            case 'mcq-expression-btn':
                mcqInputField.value = '';
                mcqInputField.placeholder = 'Enter expression and click add';
                mcqInputField.setAttribute('data-answer-type', 'e-answer');
                break;
            case 'mcq-float-btn':
                mcqInputField.value = '';
                mcqInputField.placeholder = 'Enter float and click add';
                mcqInputField.setAttribute('data-answer-type', 'f-answer');
                break;
            case 'mcq-text-btn':
                mcqInputField.value = '';
                mcqInputField.placeholder = 'Enter text and click add';
                mcqInputField.setAttribute('data-answer-type', 't-answer');
                break;
            case 'mcq-latex-btn':
                mcqInputField.value = '';
                mcqInputField.placeholder = 'Enter latex and click add';
                mcqInputField.setAttribute('data-answer-type', 'l-answer');
                break;
            default:
                // Nothing yet
        }
    })

    
    addMcqOptionBtn.addEventListener('click', (event)=>{
        event.preventDefault();
        if (mcqInputField.value === null || mcqInputField.value ==='') {
            alert('Cannot create an empty mcq option.')
            
        }
        else{
            try{
                const formatted_new_answer = create_inputed_mcq_div(mcqInputField.value, mcqInputField.dataset.answerType);
                inputedMcqAnswersDiv.appendChild(formatted_new_answer);
                mcqInputField.value = '';
                option_counter += 1;
            }
            catch(error){
                alert('Make sure you enter the correct format of the answer type you selected.')
            }
            
        }


    })

    inputedMcqAnswersDiv.addEventListener('click', (event)=>{
        event.preventDefault();
        target = event.target
        if(target.classList.contains('mcq-false')){
            target.classList.remove('mcq-false','btn-warning');
            target.classList.add('mcq-true', 'btn-info');
            target.innerHTML = 'True';
            num_true_counter += 1;
            const answer_info_input = target.parentNode.parentNode.querySelector('.answer_info');
            answer_info_input.value = rep(answer_info_input.value, 0, '1');
        } else if(target.classList.contains('mcq-true')){
            target.classList.add('mcq-false','btn-warning');
            target.classList.remove('mcq-true', 'btn-info');
            target.innerHTML = 'False'; 
            num_true_counter -= 1;    
            const answer_info_input = target.parentNode.parentNode.querySelector('.answer_info');
            answer_info_input.value = rep(answer_info_input.value, 0, '0');
        } else if (target.classList.contains('mcq-delete')){
            num_mcq_options_counter -= 1;
            if (target.classList.contains('mcq-true')){
                num_true_counter -= 1;
            }
            inputedMcqAnswersDiv.removeChild(target.parentNode.parentNode.parentNode);//TODO: Can probably make this something better.
        }
    })








    /*------------------------------------------STRUCTURAL QUESTION --------------------------------- */

    const latexAnswerDiv = `
    <div class="l-answer"><br/>
    <label>Latex Answer:</label>
        <input style="width: 100%; box-sizing: border-box;" class="question-input-field" placeholder="Enter LaTex" type="text" class="latex-answer-input" name="answer"/>
        </div>
    `
    frBtn.addEventListener('click', (event)=>{
        event.preventDefault();
        inputedMcqAnswersDiv.style.display = 'none';
        formattedAnswerDiv.innerHTML = 'Free response mode selected.'
        formattedAnswerDiv.style.display = 'block';
        mcqOptionBtnsDiv.style.display = 'none';
        mcqInputDiv.style.display = 'none';
        calculatorDiv.style.display = 'none';
        answerFieldsDiv.innerHTML = '';
        mode = 'fr-answer';  
        formattedAnswerDiv.scrollIntoView({behavior: 'smooth'});
        // Append '/4' at the end of the URL
        const newAction = currentAction + '/4';
        // Update the form's action attribute
        form.setAttribute('action', newAction);      
    })
    expressionBtn.addEventListener('click', (event)=> {
        event.preventDefault();
        inputedMcqAnswersDiv.style.display = 'none';
        formattedAnswerDiv.style.display = 'block';
        mcqOptionBtnsDiv.style.display = 'none';
        mcqInputDiv.style.display = 'none';
        calculatorDiv.style.display = 'block';
        answerFieldsDiv.innerHTML = '';
        mode = 'e-answer';
        screen.value = ''
        screen.placeholder = 'Algebraic expression';
        formattedAnswerDiv.innerHTML = ''

        answerFieldsDiv.scrollIntoView({ behavior: 'smooth' });
    
        // Append '/0' at the end of the URL
        const newAction = currentAction + '/0';
        // Update the form's action attribute
        form.setAttribute('action', newAction);

    });

    floatBtn.addEventListener('click', function(event) { 
        event.preventDefault();
        inputedMcqAnswersDiv.style.display = 'none';
        formattedAnswerDiv.style.display = 'block';
        mcqOptionBtnsDiv.style.display = 'none';
        mcqInputDiv.style.display = 'none';
        calculatorDiv.style.display = 'block';
        answerFieldsDiv.innerHTML = '';
        mode = 'f-answer';
        screen.value = ''
        screen.placeholder = 'Enter real number';
        formattedAnswerDiv.innerHTML = ''

        answerFieldsDiv.scrollIntoView({ behavior: 'smooth' });
        // Append '/1' at the end of the URL
        const newAction = currentAction + '/1';
        // Update the form's action attribute
        form.setAttribute('action', newAction);
    });

    latexBtn.addEventListener('click', (event)=> {
        event.preventDefault();
        mode = 'l-answer'
        inputedMcqAnswersDiv.style.display = 'none';
        formattedAnswerDiv.style.display = 'block';
        mcqOptionBtnsDiv.style.display = 'none';
        mcqInputDiv.style.display = 'none';
        calculatorDiv.style.display = 'none';
        screen.value = ''
        formattedAnswerDiv.innerHTML = ''
        answerFieldsDiv.innerHTML = latexAnswerDiv;
        answerFieldsDiv.scrollIntoView({ behavior: 'smooth' });
    
        // Append '/2' at the end of the URL
        const newAction = currentAction + '/2';
        // Update the form's action attribute
        form.setAttribute('action', newAction);



        // Adding event listener to the input field.
        const latexInput = answerFieldsDiv.querySelector('input');
        latexInput.addEventListener('input', ()=>{
            var answerFieldDiv = answerFieldsDiv.querySelector('div');
            var latexInputField = answerFieldDiv.querySelector('input');
            const userInputLatex = latexInputField.value;
           
            MathJax.typesetPromise().then(() => {
                try{
                    const formattedAnswer = MathJax.tex2chtml(userInputLatex + '\\phantom{}');
                    formattedAnswerDiv.innerHTML = '';
                    formattedAnswerDiv.appendChild(formattedAnswer);
                    MathJax.typesetPromise();
                } catch(error){
                    //console.log(error);
                }

              });


        })
    });

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
               // console.log(error);
            }
            
            }); 

    })
    form.addEventListener('submit', (event) => {

        if (mode==='e-answer'){
            const userInputNode = math.parse(screen.value);
            var userInputString = userInputNode.toString();
            //var userInputString = math.simplify(userInputNode, {}, {context: math.simplify.realContext}).toString()
            screen.value = userInputString;
        }
        else if(
            mode==='f-answer'
        ) {
            const userInputNode = math.parse(screen.value);
            var userInputString = userInputNode.evaluate();
            screen.value = userInputString;
            
        } else if (mode=='m-answer'){
            if(num_mcq_options_counter < 2){
                event.preventDefault();
                alert('The number of options for an MCQ must be at least 2.');
            }
            if(num_true_counter < 1){
                event.preventDefault();
                alert('Must select at least one MCQ answer as correct.');
            }

    
        }

        // Now the form will be submited
    });






function create_inputed_mcq_div(answer_value, answer_type) {
    var inputedMcqDiv = document.createElement('div'); // to be appended to .inputed-mcq-answers.
    num_mcq_options_counter += 1;
    var answer_info_encoding = '000' // First character for True or False, second for question type, and third for question_number 
    // The following is a blue print of the information stored about an mcq-option.
    // One of the hidden inputs should store the string value of the answer, as well as the type of answer it is..
    // The other hidden input will store the reference question.i.e 0 = 'main', 1 = 'a', 2 = 'b', 4 = 'c' etc. 
    //     so 0 may mean it is an mcq option for the main question. while 'b' means it is sub question.
   //      Side note: In the spirit of the definition of the django models, it's actually not possible to have an answer
   //      for 'main' given that it should only comprise of text. 
   //      
   // May add an edit button later, but I don't think it is useful.
    var formatted_answer = '';
    switch (answer_type) {
        case 'f-answer':
            display_value = answer_value;
            answer_value = math.parse(answer_value).evaluate();
            answer_info_encoding = rep(answer_info_encoding, 1, '1');
            break;
        case 't-answer':
            display_value = answer_value;
            answer_info_encoding = rep(answer_info_encoding, 1, '3');
            break;
        case 'l-answer':
            display_value = answer_value; // Actually doesn't do anything.
            answer_info_encoding = rep(answer_info_encoding, 1, '2');
            break;
        case 'e-answer':
            answer_value = math.parse(answer_value).toString();
            display_value = answer_value;
            answer_info_encoding = rep(answer_info_encoding, 1, '0');
            break;
        default:
            //
    }
    MathJax.typesetPromise().then(() => {
        var userInputLatex = '';
        try {
            if (answer_type==='l-answer'){// if latex-answer or text-answer
                userInputLatex = answer_value;
                formatted_answer = MathJax.tex2chtml(userInputLatex + '\\phantom{}');
            } else if(answer_type==='t-answer'){
                userInputLatex = answer_value;
                formatted_answer = document.createElement('p');
                formatted_answer.innerHTML = userInputLatex;
            }
            else{
                const userInputNode = math.parse(processString(display_value));
                userInputLatex = userInputNode.toTex();
                formatted_answer = MathJax.tex2chtml(userInputLatex + '\\phantom{}');
            }
            

            // Now that the formatted_answer is ready, create the necessary HTML structure
            var mcqAnswerDiv = document.createElement('div');
            mcqAnswerDiv.className = 'inputed-mcq-answer';
            mcqAnswerDiv.innerHTML = `
                <br/>
                <div class="formatted-answer"></div>
                <input value="${answer_value}" type="hidden" name="answer_value_${option_counter}"/>
                <input value="${answer_info_encoding}" type="hidden" class="answer_info" name="answer_info_${option_counter}"/>
                <div class="add-delete-btns">
                    <button type="button" class="btn btn-warning mcq-status mcq-false exempt">False</button>
                    <button  type="button" class="btn btn-danger mcq-delete exempt">delete</button>
                </div>
            `;
            
            // Append the formatted_answer element as a child
            var formattedAnswerDiv = mcqAnswerDiv.querySelector('.formatted-answer');
            formattedAnswerDiv.appendChild(formatted_answer);

            // Append mcqAnswerDiv to inputedMcqDiv
            inputedMcqDiv.appendChild(mcqAnswerDiv);
            MathJax.typesetPromise();
        } catch (error) {
            console.log(error);
        }
    });


    return inputedMcqDiv;
}



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

  
  
