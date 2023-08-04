document.addEventListener('DOMContentLoaded', () => {

    const expressionBtn = document.querySelector('#expression-btn');
    const expressionAnswerInput = document.querySelector("#expression-answer-input");
    const answerFieldsDiv = document.querySelector('.answer-fields');
    const form = document.querySelector('#question-form');
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
    });

    floatBtn.addEventListener('click', function(event) { 
        event.preventDefault();
        answerFieldsDiv.innerHTML = floatAnswerDiv;
        answerFieldsDiv.scrollIntoView({ behavior: 'smooth' })
    });


    form.addEventListener('submit', (event) => {
        event.preventDefault();
        var answerFieldDiv = answerFieldsDiv.querySelector('div');
        // TODO: make sure the user always enter the correct type of answer.

        if (answerFieldDiv.classList.contains('e-answer')){
            var expressionInputField = answerFieldDiv.querySelector('input');
            const userInputNode = math.parse(expressionInputField.value);
            var userInputString = userInputNode.toString();
            var userInputLatex = userInputNode.toTex();
            expressionInputField.value = userInputString;
            console.log(userInputLatex);
        }
        else if(
            answerFieldDiv.classList.contains('f-answer')
        ) {
            var floatInputField = answerFieldDiv.querySelector('input');
            const userInputNode = math.parse(floatInputField.value);
            var userInputString = userInputNode.evaluate();
            var userInputLatex = userInputNode.toTex();
            floatInputField.value = userInputString;
            console.log(userInputLatex);
        }
        
        // Now submit the form
        //form.submit();
    });

});