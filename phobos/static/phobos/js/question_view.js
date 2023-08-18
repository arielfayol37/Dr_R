
document.addEventListener('DOMContentLoaded', () => {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js';
    script.async = true;
    script.id = 'MathJax-script';
    document.head.appendChild(script);
    
    script.onload = () => {
        const formattedAnswerDivs = document.querySelectorAll('.formatted-answer');
        MathJax.typesetPromise().then(() => {
            formattedAnswerDivs.forEach((formattedAnswerDiv) => {
                try {
                    const inputElement = formattedAnswerDiv.querySelector('.latex-answer-question-view');
                    if (inputElement != null) {
                        var formatted_answer = MathJax.tex2chtml(inputElement.value + '\\phantom{}');
                        formattedAnswerDiv.appendChild(formatted_answer);
                        MathJax.typesetPromise();
                    }
                    /*
                    else {
                        var formatted_answer = MathJax.tex2chtml(formattedAnswerDiv.innerHTML + '\\phantom{}')
                        // TODO: Maybe should this differently...because text answers won't be displayed
                        // well, since 'and' and 'or' will be replaced with conjunction and disjunction symbol.
                        // furthermore, spaces will be removed.
                        formattedAnswerDiv.innerHTML = '';
                    }
                    
                    //inputElement.remove();

                    */
                } catch (error) {
                    console.log(error);
                }
            });
        });
    };
});


/*
document.addEventListener('DOMContentLoaded', () => {
    const latexAnswers = document.querySelectorAll('.latex-answer-question-view');
    
    // Load MathJax
    const script = document.createElement('script');
    const script2 = document.createElement('script');
    script2.type = 'text/javascript';
    script2.src = src="https://polyfill.io/v3/polyfill.min.js?features=es6"
    script.type = 'text/javascript';
    script.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js';
    script.async = true;
    document.head.appendChild(script);
    var formatted_answer = '';
    // Process LaTeX answers after MathJax is loaded
    script2.onload = () => {
        script.onload = () => {
            latexAnswers.forEach((element) => {
                MathJax.typesetPromise().then(() => {
                    try{
                        formatted_answer = MathJax.tex2chtml(element.value + '\\phantom{}');
                        element.parentNode.appendChild(formatted_answer);
                    }catch(error){
                        console.log(error)
                    }
            });})
        };
    };
    
});
*/
