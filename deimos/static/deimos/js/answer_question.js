document.addEventListener('DOMContentLoaded', ()=> {
    const answerFieldsDiv = document.querySelector('.answer-fields');
    const form = document.querySelector('#question-form');
    const validateAnswerActionURL = extractQuestionPath(window.location.href) + '/validate_answer';
    //console.log(newActionURL);
    //form.setAttribute('action', newActionURL);
    const submitBtn = document.querySelector('#submit-btn');
    const formattedAnswerDiv = document.querySelector('.formatted-answer');
    const calculatorDiv = document.querySelector('.calculator');
    const inputedMcqAnswersDiv = document.querySelector('.inputed-mcq-answers');
    var num_true_counter = 0;
    const screen = document.querySelector('#screen'); 
    const questionType = document.querySelector('.question-type');

/*-----------------------------Question submission-----------------------*/

    submitBtn.addEventListener('click', (event)=>{
        event.preventDefault();

        const yellowLight = form.querySelector('.yellow-light');
        const greenLight = form.querySelector('.green-light');
        const redLight = form.querySelector('.red-light');
        
        // For now, yellow light represents to many attempts
        if(!greenLight.classList.contains('activated') && !yellowLight.classList.contains('activated')){
          // Checking whether the submitted answer is valid
          const question_type = questionType.value
          if (question_type.startsWith('structural')){
            if(screen.value.length === 0){
              alert('Cannot submit blank answer');
              return;
            }
            const last_character = parseInt(question_type.charAt(question_type.length-1)); 
            // Checks if the answer to the question is supposed to be a float
            if(last_character===5 || last_character===1){
              try{
                const test_answer = math.evaluate(screen.value);
                if(typeof(test_answer) != 'number'){
                  
                  alert('The answer you provided is not a float');
                  return;
              }
              }catch{
                alert('The answer you provided is not a float');
                return;
              }
            }
           
          } else if (questionType.value ==='mcq' && num_true_counter===0){
            alert('Must select at least on MCQ answer as true');
            return;
          }
          scrollToCenter(redLight);
          yellowLight.classList.add('activated');
          yellowLight.classList.add('blinking');
          redLight.classList.remove('activated');
        if (question_type.startsWith('structural')){
            fetch(`/${validateAnswerActionURL}`, {
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
                body: JSON.stringify({
                        answer: math.simplify(processString(screen.value)).toString(),
                        questionType: questionType.value    
                })
              })
              .then(response => response.json())
              .then(result => {
                  // Print result
                  //console.log(result.correct);
                  if(result.previously_submitted){
                    alert('You already attempted using that answer');
                    resetLightsToRed(redLight,yellowLight,greenLight);
                    return;
                  }
                  toggleLight(result.correct,result.too_many_attempts,redLight,yellowLight,greenLight);
                  feedback_message(result.feedback_data)
              });
        } else if( question_type ==='mcq'){
            // TODO make sure some mcqs are selected as true.
            fetch(`/${validateAnswerActionURL}`, {
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
                body: JSON.stringify({
                        answer: getSelectedTrueAnswerIds(),
                        questionType: questionType.value    
                })
              })
              .then(response => response.json())
              .then(result => {
                  // Print result
                  //console.log(result.correct);
                  if(result.previously_submitted){
                    alert('You already attempted using that answer');
                    resetLightsToRed(redLight,yellowLight,greenLight);
                    return;
                  }
                  toggleLight(result.correct,result.too_many_attempts, redLight, yellowLight, greenLight);
              });
        }else {
          alert('Something went wrong');
        }
      }else if(greenLight.classList.contains('activated')){
            alert('You already passed this question')
      }
    });

/*----------------------------DISPLAYING LATEX-------------------------*/

function displayLatex(){
    const formattedAnswerDivs = document.querySelectorAll('.formatted-answer');
    MathJax.typesetPromise().then(() => {
        formattedAnswerDivs.forEach((formattedAnswerDiv) => {
            try {
                const inputElement = formattedAnswerDiv.querySelector('.latex-answer-question-view');
                if (inputElement != null){
                    const formatted_answer = MathJax.tex2chtml(inputElement.value + '\\phantom{}');
                    //inputElement.remove();
                    formattedAnswerDiv.appendChild(formatted_answer);
                    MathJax.typesetPromise();
                }

            } catch (error) {
                console.log(error);
            }
        });
    });

}

displayLatex();

    /*----------------------------MCQ QUESTION --------------------------------*/
    if (!(inputedMcqAnswersDiv === null)){
    inputedMcqAnswersDiv.addEventListener('click', (event)=>{
        event.preventDefault();
        target = event.target
        if(target.classList.contains('mcq-false')){
            target.classList.remove('mcq-false','btn-warning');
            target.classList.add('mcq-true', 'btn-info');
            target.innerHTML = 'True';
            num_true_counter += 1;
            const answer_info_input = target.parentNode.querySelector('.formatted-answer').querySelector('.answer_info');
            answer_info_input.value = rep(answer_info_input.value, 0, '1');
        } else if(target.classList.contains('mcq-true')){
            target.classList.add('mcq-false','btn-warning');
            target.classList.remove('mcq-true', 'btn-info');
            target.innerHTML = 'False'; 
            num_true_counter -= 1;    
            const answer_info_input = target.parentNode.querySelector('.formatted-answer').querySelector('.answer_info');
            answer_info_input.value = rep(answer_info_input.value, 0, '0');
        }
    })

    }

    if (!(screen === null)){

        screen.addEventListener('input', ()=> {
            MathJax.typesetPromise().then(() => {
                try {
        
                const userInputNode = math.simplify(processString(screen.value));
                var userInputLatex = userInputNode.toTex();
                const formattedAnswer = MathJax.tex2chtml(userInputLatex + '\\phantom{}');
                formattedAnswerDiv.innerHTML = '';
                formattedAnswerDiv.appendChild(formattedAnswer);
                MathJax.typesetPromise();
                } catch (error) {
                   //console.log(error);
                }
                
                }); 
        
        })
        
    }


    form.addEventListener('submit', (event)=>{
        event.preventDefault();
        if (!(screen === null)){
        const userInputNode = math.simplify(processString(screen.value));
        var userInputString = userInputNode.toString();
        screen.value = userInputString;
        }
        if (!(inputedMcqAnswersDiv === null) && num_true_counter < 1){
            event.preventDefault();
            alert('Must select at least one MCQ answer as correct.');
        }
    });


    /*------------------------------UTILITY FUNCTIONS ----------------------------*/
    function toggleLight(correct, too_many_attempts,redLight, yellowLight, greenLight) {
        // Make the yellow light blink as though the program was 'thinking';

          if (correct) {
            
            setTimeout(function () {
              // Code to execute after 1.6 seconds
              yellowLight.classList.remove('activated');
              yellowLight.classList.remove('blinking');
              greenLight.classList.add('activated');
            }, 1600);
        
          } else {
            setTimeout(function () {
              // Code to execute after 1.6 seconds
              yellowLight.classList.remove('activated');
              yellowLight.classList.remove('blinking');
              if(too_many_attempts){
                // Keep yellow light
                yellowLight.classList.add('activated');
                alert('Too many attempts for this question');
              }else {
                redLight.classList.add('activated');
              }
              
            }, 1600);
        
          }

      }
      
    function resetLightsToRed(redLight, yellowLight, greenLight){
      redLight.classList.add('activated');
      redLight.classList.remove('blinking');
      yellowLight.classList.remove('blinking');
      yellowLight.classList.remove('activated');
      greenLight.classList.remove('blinking');
      greenLight.classList.remove('activated');
    }
function rep(str, index, char) {
    str = setCharAt(str,index,char);
    return str
}

function setCharAt(str,index,chr) {
    if(index > str.length-1) return str;
    return str.substring(0,index) + chr + str.substring(index+1);
}

function extractQuestionPath(url) {
    const startIndex = url.indexOf('deimos');
    if (startIndex !== -1) {
        return url.substring(startIndex);
    } else {
        return null; // If 'courses' not found in URL
    }
}
function scrollToCenter(element) {
    const elementRect = element.getBoundingClientRect();
    const absoluteElementTop = elementRect.top + window.pageYOffset;
    const middle = absoluteElementTop - window.innerHeight / 2;
    window.scrollTo({ top: middle, behavior: 'smooth' });
  }
  

function getCookie(name) {
    if (!document.cookie) {
      return null;
    }

    const csrfCookie = document.cookie
      .split(';')
      .map(c => c.trim())
      .find(c => c.startsWith(name + '='));

    if (!csrfCookie) {
      return null;
    }

    return decodeURIComponent(csrfCookie.split('=')[1]);
  }

  function getSelectedTrueAnswerIds() {
    const mcqOptions = document.querySelectorAll('.mcq-option-answer');
    const selectedAnswerIds = [];
  
    mcqOptions.forEach((option) => {
      const answerIdInput = option.querySelector('.answer_id');
      const answerInfoInput = option.querySelector('.answer_info');
  
      if (answerIdInput && answerInfoInput && answerInfoInput.value.charAt(0) === '1') {
        selectedAnswerIds.push(answerIdInput.value);
      }
    });
  
    return selectedAnswerIds;
  }

function feedback_message(result){

  console.log(result);
}

});

