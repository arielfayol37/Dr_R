document.addEventListener('DOMContentLoaded', () => {

    const expressionBtn = document.querySelector('#expression-btn');
    const answerFieldsDiv = document.querySelector('.answer-fields');
    const form = document.querySelector('#question-form');
    let currentAction = form.getAttribute('action');
    const floatBtn = document.querySelector('#mcq-btn');
    const floatAnswerDiv = `
    
    <div class="f-answer"><br/>
    <label>Asnswer:</label>
              <input placeholder="Enter a real number" type="text" id="float-answer-input" name="answer"/>
            </div>
    `
    const expressionAnswerDiv = `
    
    <div class="e-answer"><br/>
    <label>Asnswer:</label>
              <input placeholder="Enter algebraic expression" type="text" id="expression-answer-input" name="answer"/>
            </div>
    `
    expressionBtn.addEventListener('click', (event)=> {
        event.preventDefault();
        answerFieldsDiv.innerHTML = expressionAnswerDiv;
        answerFieldsDiv.scrollIntoView({ behavior: 'smooth' });
    
        // Append '/0' at the end of the URL
        const newAction = currentAction + '/0';
        // Update the form's action attribute
        form.setAttribute('action', newAction);

    });

    floatBtn.addEventListener('click', function(event) { 
        event.preventDefault();
        answerFieldsDiv.innerHTML = floatAnswerDiv;
        answerFieldsDiv.scrollIntoView({ behavior: 'smooth' });
        // Append '/1' at the end of the URL
        const newAction = currentAction + '/1';
        // Update the form's action attribute
        form.setAttribute('action', newAction);
    });


    form.addEventListener('submit', (event) => {
        var answerFieldDiv = answerFieldsDiv.querySelector('div');
        // TODO: make sure the user always enter the correct type of answer.

        if (answerFieldDiv.classList.contains('e-answer')){
            var expressionInputField = answerFieldDiv.querySelector('input');
            const userInputNode = math.parse(expressionInputField.value);
            var userInputString = userInputNode.toString();
            var userInputLatex = userInputNode.toTex();
            expressionInputField.value = userInputString;
        }
        else if(
            answerFieldDiv.classList.contains('f-answer')
        ) {
            var floatInputField = answerFieldDiv.querySelector('input');
            const userInputNode = math.parse(floatInputField.value);
            var userInputString = userInputNode.evaluate();
            var userInputLatex = userInputNode.toTex();
            floatInputField.value = userInputString;
            
        }
        
        // Now the form will be submited

    });

});