document.addEventListener('DOMContentLoaded', () => {

    const expressionBtn = document.querySelector('#expression-btn');
    const answerFieldsDiv = document.querySelector('.answer-fields');
    const form = document.querySelector('#question-form');
    let currentAction = form.getAttribute('action');
    const floatBtn = document.querySelector('#float-btn');
    const latexBtn = document.querySelector('#latex-btn');
    const formattedAnswerDiv = document.querySelector('#formatted-answer');
    const screen = document.querySelector('#screen'); 
    const calculatorDiv = document.querySelector('.calculator');
    calculatorDiv.style.display = 'none';
    let mode = '';

    const latexAnswerDiv = `
    <div class="l-answer"><br/>
    <label>Latex Answer:</label>
        <input style="width: 100%; box-sizing: border-box;" placeholder="Enter LaTex" type="text" id="latex-answer-input" name="answer"/>
        </div>
    `
    expressionBtn.addEventListener('click', (event)=> {
        event.preventDefault();
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
        calculatorDiv.style.display = 'none';
        screen.value = ''
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
                    const formattedAnswer = MathJax.tex2chtml(userInputLatex + '\\phantom{}');
                    formattedAnswerDiv.innerHTML = '';
                    formattedAnswerDiv.appendChild(formattedAnswer);
                } catch(error){
                    //console.log(error);
                }

              });


        })
    });

    screen.addEventListener('input', ()=> {
        /*
        if(mode==='f-answer'){
            MathJax.typesetPromise().then(() => {
            try {

            const userInputNode = math.parse(processString(screen.value));
            var userInputLatex = userInputNode.toTex();
            const formattedAnswer = MathJax.tex2chtml(userInputLatex + '\\phantom{}');
            formattedAnswerDiv.innerHTML = '';
            formattedAnswerDiv.appendChild(formattedAnswer);
            } catch (error) {
               // console.log(error);
            }
            
            });            
        }
        else if(mode==='e-answer'){
            MathJax.typesetPromise().then(() => {
                try {
                    const userInputNode = math.parse(processString(screen.value));
                    var userInputLatex = userInputNode.toTex();
                    const formattedAnswer = MathJax.tex2chtml(userInputLatex + '\\phantom{}');
                    formattedAnswerDiv.innerHTML = '';
                    formattedAnswerDiv.appendChild(formattedAnswer);

                } catch (error){
                   // console.log(error);
                }

              });            
        }
        */
        MathJax.typesetPromise().then(() => {
            try {

            const userInputNode = math.parse(processString(screen.value));
            var userInputLatex = userInputNode.toTex();
            const formattedAnswer = MathJax.tex2chtml(userInputLatex + '\\phantom{}');
            formattedAnswerDiv.innerHTML = '';
            formattedAnswerDiv.appendChild(formattedAnswer);
            } catch (error) {
               // console.log(error);
            }
            
            }); 

    })
    form.addEventListener('submit', (event) => {

        if (mode==='e-answer'){
            const userInputNode = math.parse(screen.value);
            var userInputString = userInputNode.toString();
            screen.value = userInputString;
        }
        else if(
            mode==='f-answer'
        ) {
            const userInputNode = math.parse(screen.value);
            var userInputString = userInputNode.evaluate();
            screen.value = userInputString;
            
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

  
  