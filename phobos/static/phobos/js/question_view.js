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
                    const inputElement = formattedAnswerDiv.querySelector('.hidden_answer');
                    const preface = formattedAnswerDiv.querySelector('.preface');
                    const units = formattedAnswerDiv.querySelector('.units');
                    if (inputElement != null) {
                        if(inputElement.classList.contains('latex')){
                            const latex = inputElement.value;
                            const answer_latex = MathJax.tex2chtml(latex + '\\phantom{}');
                            var formatted_answer = `<span>${answer_latex.innerHTML}</span>`;
                        } else if(inputElement.classList.contains('mcq-expression')){
                            const latex = math.parse(inputElement.value).toTex();
                            const answer_latex = MathJax.tex2chtml(latex + '\\phantom{}');
                            var formatted_answer = `<span>${answer_latex.innerHTML}</span>`;
                        } 
                        else {
                            const latex = math.parse(inputElement.value).toTex();
                            const units_latex = MathJax.tex2chtml(units.value);
                            const preface_latex = MathJax.tex2chtml(preface.value);
                            const answer_latex = MathJax.tex2chtml(latex + '\\phantom{}');
                            var formatted_answer = `<span>${preface_latex.innerHTML}</span> 
                                                        <span>${answer_latex.innerHTML}</span>
                                                        <span>${units_latex.innerHTML}</span>`;
                        }
                        
                        formattedAnswerDiv.innerHTML = formatted_answer;
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



