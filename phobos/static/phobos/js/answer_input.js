document.addEventListener('DOMContentLoaded', () => {

    const expressionBtn = document.querySelector('#expression-btn');
    const answerLabel = document.querySelector('.answer-fields').querySelector('label');
    const expressionAnswerInput = document.querySelector("#expression-answer-input");
    const floatAnswerInput = document.querySelector("#float-answer-input");
    const form = document.querySelector('#question-form');
    const floatBtn = document.querySelector('#mcq-btn');
    answerLabel.style.display = 'none';
    expressionAnswerInput.style.display = 'none';
    floatAnswerInput.style.display = 'none';
    expressionBtn.addEventListener('click', (event)=> {
        event.preventDefault();
        expressionAnswerInput.style.display = 'block';
        floatAnswerInput.style.display = 'none';
        expressionAnswerInput.scrollIntoView({ behavior: 'smooth' });
    });

    floatBtn.addEventListener('click', function(event) { 
        event.preventDefault();
        expressionAnswerInput.style.display = 'none';
        floatAnswerInput.style.display = 'block';
    });

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        
        // Get the user's input from the input field
        const userInput = expressionAnswerInput.value;
        var parsedInput ;
        try {
            parsedInput = math.evaluate(`${userInput}`);
        }catch (error){
            parsedInput = math.evaluate(`'${userInput}'`);
        }
        

        // Set the parsed value as the input's value
        expressionAnswerInput.value = parsedInput;
        console.log(parsedInput);
        // Now submit the form
        //form.submit();
    });

});