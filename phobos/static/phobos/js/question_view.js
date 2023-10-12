document.addEventListener('DOMContentLoaded', () => {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js';
    script.async = true;
    script.id = 'MathJax-script';
    document.head.appendChild(script);
    
    script.onload = () => {
        const formattedAnswerDivs = document.querySelectorAll('.formatted-answer-option');
        MathJax.typesetPromise().then(() => {
            formattedAnswerDivs.forEach((formattedAnswerDiv) => {

                try {
                    const inputElement = formattedAnswerDiv.querySelector('.latex-answer-question-view');
                    if (inputElement != null) {
                        var formatted_answer = MathJax.tex2chtml(inputElement.value + '\\phantom{}');
                        formattedAnswerDiv.appendChild(formatted_answer);
                        MathJax.typesetPromise();
                    }
                } catch (error) {
                    console.log(error);
                }
            });
        });
    
    
    const questionContentPs = document.querySelectorAll(".question-content");
    MathJax.typesetPromise().then(() => {

        questionContentPs.forEach((questionContentP) => {
            try{
                questionContentP.innerHTML = parseLatex(questionContentP.innerHTML);
                
            } catch(error){
                console.log(error)
            }
        })
        MathJax.typesetPromise();
    })
        
    function parseLatex(text) {
        const latexPattern = /#{(.*?)}#/g;
        
        var formattedText = text.replace(latexPattern, (_, latexCode) => {
            try {
                const mathJaxHTML = MathJax.tex2chtml(latexCode + '\\phantom{}');
                return mathJaxHTML.innerHTML;
            } catch (error) {
                console.log(error);
                return ''; // Return an empty string if MathJax conversion fails.
            }
        });
    
        return formattedText;
    }

    };
});



