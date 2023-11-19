document.addEventListener('DOMContentLoaded', ()=>{
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
})