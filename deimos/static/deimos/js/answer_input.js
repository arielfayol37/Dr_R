document.addEventListener('DOMContentLoaded', ()=> {
    const answerFieldsDiv = document.querySelector('.answer-fields');
    const form = document.querySelector('#question-form');
    let currentAction = form.getAttribute('action');
    const formattedAnswerDiv = document.querySelector('#formatted-answer');
    const calculatorDiv = document.querySelector('.calculator');
    const screen = document.querySelector('#screen'); 
    
    screen.addEventListener('input', ()=> {
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

    form.addEventListener('submit', (event)=>{
        const userInputNode = math.parse(screen.value);
        var userInputString = userInputNode.toString();
        screen.value = userInputString;
    });


});
