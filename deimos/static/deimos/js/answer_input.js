document.addEventListener('DOMContentLoaded', ()=> {
    const answerFieldsDiv = document.querySelector('.answer-fields');
    const form = document.querySelector('#question-form');
    let currentAction = form.getAttribute('action');
    const formattedAnswerDiv = document.querySelector('.formatted-answer');
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
               console.log(error);
            }
            
            }); 
    
    })

    form.addEventListener('submit', (event)=>{
        const userInputNode = math.parse(screen.value);
        var userInputString = userInputNode.toString();
        screen.value = userInputString;
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
