document.addEventListener('DOMContentLoaded', () => {

    const expressionBtn = document.querySelector('#expression-btn');
    const answerFieldsDiv = document.querySelector('.answer-fields');
    const form = document.querySelector('#question-form');
    let currentAction = form.getAttribute('action');
    const floatBtn = document.querySelector('#float-btn');
    const latexBtn = document.querySelector('#latex-btn');
    const formattedAnswerDiv = document.querySelector('#formatted-answer');
    const floatAnswerDiv = `
    
    <div class="f-answer"><br/>
    <label>Float Asnswer:</label>
              <input placeholder="Enter a real number" type="text" id="float-answer-input" name="answer"/>
            </div>
    `
    const expressionAnswerDiv = `
    
    <div class="e-answer"><br/>
    <label>Expression Asnswer:</label>
              <input placeholder="Enter algebraic expression" type="text" id="expression-answer-input" name="answer"/>
            </div>
    `
    const latexAnswerDiv = `
    <div class="l-answer"><br/>
    <label>Latex Answer:</label>
        <input placeholder="Enter LaTex" type="text" id="latex-answer-input" name="answer"/>
        </div>
    `
    expressionBtn.addEventListener('click', (event)=> {
        event.preventDefault();
        formattedAnswerDiv.innerHTML = ''
        answerFieldsDiv.innerHTML = expressionAnswerDiv;
        answerFieldsDiv.scrollIntoView({ behavior: 'smooth' });
    
        // Append '/0' at the end of the URL
        const newAction = currentAction + '/0';
        // Update the form's action attribute
        form.setAttribute('action', newAction);


        // Adding event listener to the input field.
        const expressionInput = answerFieldsDiv.querySelector('input');
        expressionInput.addEventListener('input', ()=>{
            MathJax.typesetPromise().then(() => {
                try {
                    const userInputNode = math.parse(expressionInput.value);
                    var userInputLatex = userInputNode.toTex();
                    const formattedAnswer = MathJax.tex2chtml(userInputLatex);
                    formattedAnswerDiv.innerHTML = '<p>User\'s view: </p>';
                    formattedAnswerDiv.appendChild(formattedAnswer);

                } catch (error){
                    console.log(error);
                }

              });

        })

    });

    floatBtn.addEventListener('click', function(event) { 
        event.preventDefault();
        formattedAnswerDiv.innerHTML = ''
        answerFieldsDiv.innerHTML = floatAnswerDiv;
        answerFieldsDiv.scrollIntoView({ behavior: 'smooth' });
        // Append '/1' at the end of the URL
        const newAction = currentAction + '/1';
        // Update the form's action attribute
        form.setAttribute('action', newAction);

        // Adding event listener to the input field.
        const floatInput = answerFieldsDiv.querySelector('input');
        floatInput.addEventListener('input', ()=>{
            MathJax.typesetPromise().then(() => {
                try {

                const userInputNode = math.parse(floatInput.value);
                var userInputLatex = userInputNode.toTex();
                const formattedAnswer = MathJax.tex2chtml(userInputLatex);
                formattedAnswerDiv.innerHTML = '<p>User\'s view: </p>';
                formattedAnswerDiv.appendChild(formattedAnswer);
                } catch (error) {
                    // console.log(error);
                }
                
              });

        })
    });

    latexBtn.addEventListener('click', (event)=> {
        event.preventDefault();
        formattedAnswerDiv.innerHTML = ''
        answerFieldsDiv.innerHTML = latexAnswerDiv;
        answerFieldsDiv.scrollIntoView({ behavior: 'smooth' });
    
        // Append '/0' at the end of the URL
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
                    const formattedAnswer = MathJax.tex2chtml(userInputLatex);
                    formattedAnswerDiv.innerHTML = '<p>User\'s view: </p>';
                    formattedAnswerDiv.appendChild(formattedAnswer);
                } catch(error){
                    //console.log(error);
                }

              });

        })
    });


    form.addEventListener('submit', (event) => {
        var answerFieldDiv = answerFieldsDiv.querySelector('div');
        // TODO: make sure the user always enter the correct type of answer.

        if (answerFieldDiv.classList.contains('e-answer')){
            var expressionInputField = answerFieldDiv.querySelector('input');
            const userInputNode = math.parse(expressionInputField.value);
            var userInputString = userInputNode.toString();
            expressionInputField.value = userInputString;
        }
        else if(
            answerFieldDiv.classList.contains('f-answer')
        ) {
            var floatInputField = answerFieldDiv.querySelector('input');
            const userInputNode = math.parse(floatInputField.value);
            var userInputString = userInputNode.evaluate();
            floatInputField.value = userInputString;
            
        }
        /*
        else if(
            answerFieldDiv.classList.contains('l-answer')
        ) {
            var latexInputField = answerFieldDiv.querySelector('input');
            const userInputLatex = latexInputField.value;
            const formattedAnswerDiv = document.querySelector('#formatted-answer');
            MathJax.texReset();
            const formattedAnswer = MathJax.tex2chtml(userInputLatex);
            formattedAnswerDiv.innerHTML = '<p>User-Friendly Answer:</p>';
            formattedAnswerDiv.appendChild(formattedAnswer);
            
        }*/
        // Now the form will be submited

    });

});