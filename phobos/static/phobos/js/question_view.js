
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
    };
});



