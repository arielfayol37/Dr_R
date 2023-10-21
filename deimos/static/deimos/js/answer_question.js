document.addEventListener('DOMContentLoaded', ()=> {
    const forms = document.querySelectorAll('.question-form');
    //const validateAnswerActionURL = extractQuestionPath(window.location.href) + '/validate_answer';
    const screen = document.querySelector('#screen'); 
    var formattedAnswerDiv;
   
  // displaying previous submissions

  const previousAttempts = document.querySelectorAll('.previous-attempts');
  if(previousAttempts){

    MathJax.typesetPromise().then(()=>{

      previousAttempts.forEach((pA)=>{

        const elements = pA.querySelectorAll(".p-attempt");

        if (elements.length != 0){

          // /console.log(elements);
        function showElement(currentIndex, newIndex) {
          elements[currentIndex].style.top = '-100%'; // Move the current element up and out of view
          elements[currentIndex].style.opacity = '0'; // Fade it out
      
          elements[newIndex].style.top = '0'; // Move the target element to the viewable area
          elements[newIndex].style.opacity = '1'; // Fade it in
      
          pA.querySelector('.attempts-container').dataset.index = newIndex; // Update the dataset
      }
      
      pA.querySelector('.btn-attempt-down').addEventListener('click', () => {
          let currentIndex = parseInt(pA.querySelector('.attempts-container').dataset.index);
          let nextIndex = (currentIndex + 1) % elements.length;
          showElement(currentIndex, nextIndex);
      });
      
      pA.querySelector('.btn-attempt-up').addEventListener('click', () => {
          let currentIndex = parseInt(pA.querySelector('.attempts-container').dataset.index);
          let prevIndex = (currentIndex - 1 + elements.length) % elements.length;
          showElement(currentIndex, prevIndex);
      });
      

      pA.querySelector('.open-attempts').addEventListener('click', (event)=>{
        if(event.target.classList.contains('closed')){
          pA.querySelector('.a-container').style.display = 'flex';
          event.target.classList.remove('closed');
        }else{
          pA.querySelector('.a-container').style.display = 'none';
          event.target.classList.add('closed');
        }
      })

      try{
        pA.querySelectorAll('.p-attempt').forEach((p)=>{
          const content = math.parse(p.querySelector('.attempt-content').value).toTex();
          const aUnits = p.querySelector('.attempt-units');
          var finalDisplay = content
          if(aUnits != null){
            finalDisplay = content + ' ' + aUnits.value
          }
          p.innerHTML = MathJax.tex2chtml(finalDisplay).innerHTML // ; 
        })

      }catch (error){
        console.log(error);
      }
        }

      })
      MathJax.typesetPromise();
    })

  }




  // Displaying the validated submissions
    MathJax.typesetPromise().then(() => {
      const passedAnswers = document.querySelectorAll('.passed-answer');
      passedAnswers.forEach((passedAnswer)=>{
        try {
          var toDisplay = passedAnswer.querySelector('.passed-answer-content').value;
          const tUnits = passedAnswer.querySelector('.passed-answer-units');
          if(tUnits != null){
            toDisplay = toDisplay + ' ' + tUnits.value
          }
          const latex = math.parse(toDisplay).toTex()
          passedAnswer.innerHTML = MathJax.tex2chtml(latex).innerHTML;
      } catch (error) {
          console.log(error);
      }
      })
      MathJax.typesetPromise();
    });
     

    // GRADING SHEMES
    var previousGNumber = 0;
    const selectGrading = document.querySelector('.select-grading');
    const allGradingSchemes = document.querySelectorAll('.settings-modification');
    var gCounter = 0;
    allGradingSchemes.forEach((gs)=>{
      const newOption = document.createElement('option');
      newOption.value = gCounter;
      newOption.innerHTML = `Part ${String.fromCharCode(64 + gCounter + 1)}`;
      selectGrading.appendChild(newOption);
      gCounter += 1
    })
 
    selectGrading.addEventListener('change', (event)=>{
      document.querySelector(`.grading-number-${previousGNumber}`).style.display = 'none';
      document.querySelector(`.grading-number-${event.target.value}`).style.display = 'flex';
      previousGNumber = event.target.value;
    })




    // Notes variables
    const questionAddImgBtn = document.querySelector('.main-question-add-image-btn');
    const uploadedQuestionPreview = document.querySelector('.uploaded-question-preview');
    const mainQuestionImageInput = document.querySelector('.main-question-image-input');
    const mainQuestionImagePreview = document.querySelector('.main-question-image-preview');
    const questionImgUploadSection = document.querySelector('.question-image-upload-section');
    const addQuestionImgBtn = document.querySelector('.question-image-add');
    var question_img_counter = 0;
    var answer_struct;
/*-----------------------------Question submission-----------------------*/
forms.forEach((form)=>{
  var submitBtn = form.querySelector('.submit-btn');
  const inputedMcqAnswersDiv = form.querySelector('.inputed-mcq-answers');
  const hintsContainerDiv = form.querySelector('.hints-container');
  const feedbackContainerDiv = form.querySelector('.feedback-container');

  feedbackContainerDiv.querySelector('.show-feedback-btn').addEventListener('click', (event)=>{
    event.preventDefault();
    if(event.target.classList.contains('closed-feedback')){
      feedbackContainerDiv.querySelector('.formatted-answer-option').style.display = 'block';
      event.target.classList.remove('closed-feedback');
    }else{
      feedbackContainerDiv.querySelector('.formatted-answer-option').style.display = 'none';
      event.target.classList.add('closed-feedback');
    }
  })

  if(hintsContainerDiv != null){
    const questionHintsDiv = hintsContainerDiv.querySelector('.question-hints');
    const seeMoreBtn = hintsContainerDiv.querySelector('.see-more-hint-btn');
    const showHintBtn = hintsContainerDiv.querySelector('.show-hint-btn');
    if((seeMoreBtn != null) && (showHintBtn != null)){
      showHintBtn.addEventListener('click', (event)=>{
        event.preventDefault();
        if(showHintBtn.classList.contains('closed-hints')){
          questionHintsDiv.style.display = 'block';
          showHintBtn.classList.remove('closed-hints');
          showHintBtn.name = 'caret-down-outline';
          if(questionHintsDiv.dataset.counter > questionHintsDiv.dataset.seen){
            seeMoreBtn.style.display = 'block';
          }else{
            seeMoreBtn.style.display = 'none';
          }
        }else{
          questionHintsDiv.style.display = 'none';
          showHintBtn.classList.add('closed-hints');
          showHintBtn.name = 'caret-forward-outline';
        }
      })
      seeMoreBtn.addEventListener('click', (event)=>{
        event.preventDefault();
        const holder = questionHintsDiv.dataset.seen;
        questionHintsDiv.dataset.seen = `${parseInt(holder) + 1}`;
        const hClass = `.hint-num-${parseInt(holder)}`
        // console.log(hClass)
        questionHintsDiv.querySelector(hClass).style.display='block';
        if(questionHintsDiv.dataset.counter > questionHintsDiv.dataset.seen){
          seeMoreBtn.style.display = 'block';
        }else{
          seeMoreBtn.style.display = 'none';
        }
    
      })
    }

  }

  
  submitBtn.addEventListener('click', (event)=>{
    event.preventDefault();
    if(submitBtn.classList.contains('attempt-mode')){
      // Changing the button from "Attempt" to "Submit answer"
      submitBtn.classList.remove('attempt-mode');
      submitBtn.classList.remove('btn-outline-success');
      submitBtn.classList.add('btn-success');
      submitBtn.value = 'Submit answer';

      // Displaying the calculator (the assumption here is that only structural questions 
      // will have an attempt-mode)
      const calculatorDiv = screen.closest('#calc-container');
      const previousForm = screen.closest('.question-form');
      if(previousForm !=null){
        const prevSubmitBtn = previousForm.querySelector('.submit-btn');
        prevSubmitBtn.value = 'Attempt';
       // prevSubmitBtn.remove('btn-success');
        prevSubmitBtn.classList.add('attempt-mode');
        //prevSubmitBtn.classList.add('btn-outline-success');
        //console.log(prevSubmitBtn);

        previousForm.querySelector('.inputed_answer_structural').value = screen.value;
        previousForm.querySelector('.inputed_units_structural').value = calculatorDiv.querySelector('.units-screen').value;
      }
      
      form.appendChild(calculatorDiv);
      screen.scrollIntoView({behavior: 'smooth'});
      calculatorDiv.classList.remove('hide');
      calculatorDiv.querySelector('.preface-content').innerHTML = form.querySelector('.answer_preface').value
      screen.value = form.querySelector('.inputed_answer_structural').value;
      if(form.querySelector('.show_screen').classList.contains('show')){
        screen.disabled = false;
        //console.log('screen enabled');
      }else{
        screen.disabled = true;
        screen.value = form.querySelector('.hidden_last_attempt_content').value
        //console.log('screen disabled');
      }
      if(form.querySelector('.show_unit').classList.contains('show')){
        const iUsInputField = form.querySelector('.inputed_units_structural');
        calculatorDiv.querySelector('.units-screen').value = iUsInputField.value
        calculatorDiv.querySelector('.units-section').style.display='block';
        if(form.querySelector('.able_unit').classList.contains('able')){
          calculatorDiv.querySelector('.units-screen').disabled = false;
          //console.log('units screen enabled');
        }else{
          const uScreen = calculatorDiv.querySelector('.units-screen')
          uScreen.value = form.querySelector('.hidden_units_last_attempt_content').value
          uScreen.disabled = true;
          //console.log('units screen disabled');
        }
      }else{
        calculatorDiv.querySelector('.units-section').style.display='none';
      }
      screen.dataset.changedPart = 'true';


      return;  
    }

    const calculatorDiv = screen.closest('#calc-container');
    var requiresUnits, submitted_units;
    if(calculatorDiv.querySelector('.units-section').style.display === 'block'){
      submitted_units = calculatorDiv.querySelector('.units-screen').value 
      requiresUnits = true;
      // console.log(`Requires units: ${requiresUnits}`);
    }else{
      submitted_units = ''
      requiresUnits = false;
      // console.log(`Requires units: ${requiresUnits}`);
    }
    
    const yellowLight = form.querySelector('.yellow-light');
    const greenLight = form.querySelector('.green-light');
    const redLight = form.querySelector('.red-light');
    const blueLight = form.querySelector('.blue-light'); // May be NULL
    
    // For now, red light represents to many attempts
    if(!greenLight.classList.contains('activated')){
      // Checking whether the submitted answer is valid
      const questionType = form.querySelector('.question-type');
      const question_type = questionType.value
      if (question_type.startsWith('structural')){
        if(screen.value.length === 0 && form.querySelector('.show_screen').classList.contains('show')){
          alert('Cannot submit blank answer');
          return;
        }
        if(requiresUnits && submitted_units.length < 1 && form.querySelector('.able_unit').classList.contains('able')){
          alert('You must provide units');
          return;
        }
        const last_character = parseInt(question_type.charAt(question_type.length-1)); 
        // Checks if the answer to the question is supposed to be a float
        if(last_character===5 || last_character===1){
          try{
            const test_answer = math.evaluate(processString(screen.value));
            if(typeof(test_answer) != 'number'){
              
              alert('The answer you provided is not a float');
              return;
          }
          }catch{
            alert('The answer you provided is not a float');
            return;
          }
        }
        try{
          answer_struct = math.simplify(processString(screen.value));
        }catch{
          alert('Enter a valid expression');
          return;
        }
       
      } else if (questionType.value ==='mcq' && inputedMcqAnswersDiv.trueCounter===0){
        alert('Must select at least on MCQ answer as true');
        return;
      }
      scrollToCenter(redLight);
      yellowLight.classList.add('activated');
      yellowLight.classList.add('blinking');
      redLight.classList.remove('activated');
      const qid = form.querySelector('.question-id').value;
      const baseUrl = window.location.href.replace(/#$/, '');
    if (question_type.startsWith('structural')){
        fetch(`${baseUrl}/validate_answer/${qid}`, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            body: JSON.stringify({
                    answer: answer_struct.toString(),
                    submitted_answer: screen.value,
                    questionType: questionType.value,
                    submitted_units: submitted_units    
            })
          })
          .then(response => response.json())
          .then(result => {
              // Print result
              //console.log(result.correct);
              if(result.previously_submitted){
                alert('You already attempted using that answer');
                removeAllLights(redLight,yellowLight,greenLight, blueLight);
                return;
              }
              if(requiresUnits){
                toggleLight(result.correct,result.too_many_attempts,redLight,yellowLight,
                  greenLight,blueLight,result.units_correct, is_mcq=false, units_too_many_attempts=
                  result.units_too_many_attempts);
              }else{
                toggleLight(result.correct,result.too_many_attempts,redLight,yellowLight,
                  greenLight,blueLight, units_correct=false, is_mcq=false,units_too_many_attempts=false);
              }
              
              if(!result.correct && result.feedback_data.length > 0){
                displayFeedback(feedbackContainerDiv, result.feedback_data);
              }
              if(result.correct){
                screen.disabled = true;
                form.querySelector('.show_screen').classList.remove('show');
                // console.log(`Requires units: ${requiresUnits}`);
                if(requiresUnits){
                  if(result.units_correct){
                    setTimeout(()=>{
                      submitBtn.style.display = 'none';
                    }, 1200)

                  }else if(!result.units_too_many_attempts){
                    submitBtn.value = 'Submit units';
                    displayFeedback(feedbackContainerDiv, "Correct answer, wrong units.");
                  }
                  
                }else {
                  setTimeout(()=>{
                    submitBtn.style.display = 'none';
                  }, 1200)
                  
                }
                
              }

              if(requiresUnits){
                if(result.units_correct){
                  const uScreen = calculatorDiv.querySelector('.units-screen')
                  uScreen.disabled = true;
                  if(!result.correct){
                    displayFeedback(feedbackContainerDiv, 'Wrong answer, correct units.');
                  }
                }
              }

              if(result.too_many_attempts){
                screen.disabled = true;
                form.querySelector('.show_screen').classList.remove('show');
                if(!result.units_too_many_attempts){ // the toggle function will take care of 
                                                     // the alert message if the units attempts
                                                    //  are exceeded too.
                  displayFeedback(feedbackContainerDiv, 'You exhausted your attempts for this question. Screen is now disabled');
                  submitBtn.style.display = 'none';
                }
                
              }
              // // console.log(`units_too_many_attempts: ${result.units_too_many_atempts}`);
              if(result.units_too_many_attempts){
                form.querySelector('.able_unit').classList.remove('able');
                calculatorDiv.querySelector('.units-screen').disabled = true;
                displayFeedback(feedbackContainerDiv, 'You exhausted your units attempts for this question');
              }
          });
    } else if( question_type ==='mcq'){
        // TODO make sure some mcqs are selected as true.
        const ids_ = getSelectedTrueAnswerIds(form)
        fetch(`${baseUrl}/validate_answer/${qid}`, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            body: JSON.stringify({
                    answer: ids_,
                    questionType: questionType.value,
                    submitted_answer: ids_    
            })
          })
          .then(response => response.json())
          .then(result => {
              // Print result
              //console.log(result.correct);
              if(result.previously_submitted){
                alert('You already attempted using that answer');
                removeAllLights(redLight,yellowLight,greenLight, blueLight);
                return;
              }
              toggleLight(result.correct, result.too_many_attempts, redLight, yellowLight, greenLight);
              if(result.correct){
                submitBtn.style.display = 'none';
              }
          });
    }else {
      alert('Something went wrong');
    }
  }else if(greenLight.classList.contains('activated')){
    displayFeedback(feedbackContainerDiv, 'You already passed this question');
        //alert('You already passed this question')
  }
});



    /*----------------------------MCQ QUESTION --------------------------------*/
    if (!(inputedMcqAnswersDiv === null)){
      inputedMcqAnswersDiv.addEventListener('click', (event)=>{
          event.preventDefault();
          target = event.target
          if(target.classList.contains('mcq-false')){
              target.classList.remove('mcq-false','btn-warning');
              target.classList.add('mcq-true', 'btn-info');
              target.innerHTML = 'True';
              const holder = inputedMcqAnswersDiv.dataset.trueCounter;
              inputedMcqAnswersDiv.dataset.trueCounter =  `${parseInt(holder) + 1}`;
              const answer_info_input = target.closest('.mcq-option-answer').querySelector('.formatted-answer-option').querySelector('.answer_info');
              answer_info_input.value = rep(answer_info_input.value, 0, '1');
          } else if(target.classList.contains('mcq-true')){
              target.classList.add('mcq-false','btn-warning');
              target.classList.remove('mcq-true', 'btn-info');
              target.innerHTML = 'False'; 
              const holder = inputedMcqAnswersDiv.dataset.trueCounter;
              inputedMcqAnswersDiv.dataset.trueCounter =  `${parseInt(holder) - 1}`;
              const answer_info_input = target.closest('.mcq-option-answer').querySelector('.formatted-answer-option').querySelector('.answer_info');
              answer_info_input.value = rep(answer_info_input.value, 0, '0');
          }
      })
  
      }

})


/*----------------------------DISPLAYING LATEX-------------------------*/

function displayLatex(){
    const formattedAnswerDivs = document.querySelectorAll('.formatted-answer-option');
    MathJax.typesetPromise().then(() => {
        formattedAnswerDivs.forEach((formattedAnswerDiv) => {
            try {
                const inputElement = formattedAnswerDiv.querySelector('.latex-answer-question-view');
                if (inputElement != null){
                    const formatted_answer = MathJax.tex2chtml(inputElement.value + '\\phantom{}');
                    //inputElement.remove();
                    formattedAnswerDiv.appendChild(formatted_answer);
                    
                }

            } catch (error) {
                //console.log(error);
            }
        });
        MathJax.typesetPromise();
    });

}

displayLatex();

function displayFeedback(feedbackContainerDiv, message){
  const fO = feedbackContainerDiv.querySelector('.formatted-answer-option')
  feedbackContainerDiv.querySelector('.show-feedback-btn').style.display='block';
  fO.innerHTML = message;
  fO.style.display = 'block';
  if(message != ""){
    fO.classList.add('animate-border');
    setTimeout(()=>{
      fO.classList.remove('animate-border'); // remove animation after 3 seconds
    }, 3000)
  }
}

    if (!(screen === null)){

        screen.addEventListener('input', ()=> {
          if(screen.dataset.changedPart === 'true'){
            formattedAnswerDiv = screen.closest('.question-form').querySelector('.formatted-answer');
            screen.dataset.changedPart = 'false';
          }
          
            if(screen.value.length != 0){

              MathJax.typesetPromise().then(() => {
                try {
                var processed = processString(screen.value)
                var userInputNode = math.simplify(processed);
                var parsedNode = math.parse(processed);
                var userInputLatex = parsedNode.toTex() + '\\quad = \\quad' + userInputNode.toTex();
                const formattedAnswer = MathJax.tex2chtml(userInputLatex + '\\phantom{}');
                
                formattedAnswerDiv.innerHTML = '';
                formattedAnswerDiv.appendChild(formattedAnswer);
                MathJax.typesetPromise();
                } catch (error) {
                  // console.log(error);
                }
                
                });
            }else {
              formattedAnswerDiv.innerHTML = '';
            }
 
        
        })
        
    }



    /*------------------------------UTILITY FUNCTIONS ----------------------------*/
    function toggleLight(correct, too_many_attempts, redLight, yellowLight,
       greenLight, blueLight, units_correct=true, is_mcq=true, units_too_many_attempts=false) {
        // Make the yellow light blink as though the program was 'thinking';
        removeAllLights(redLight, yellowLight, greenLight, blueLight);
        yellowLight.classList.add('activated');
        yellowLight.classList.add('blinking');
          if (correct && units_correct) {
            
            setTimeout(function () {
              // Code to execute after 1 seconds
              yellowLight.classList.remove('activated');
              yellowLight.classList.remove('blinking');
              greenLight.classList.add('activated');
            }, 1000);
        
          } else {
            setTimeout(function () {
              // Code to execute after 1 seconds
              yellowLight.classList.remove('activated');
              yellowLight.classList.remove('blinking');

              if(too_many_attempts && units_too_many_attempts){
                redLight.classList.add('activated');
               // alert('Too many attempts for this question. Screen is now disabled');
              
              }else{

                if(units_too_many_attempts){
                //  alert('Units attempts exhausted. Units screen is now disabled.')
                }

                if(correct){
                  // This means that the units were wrong
                  if(blueLight){
                    blueLight.classList.add('activated');
                    // alert('Correct answer, but wrong units');
                  }else {
                    greenLight.classList.add('activated');
                  }
                  
                }else{
                  if(units_correct && !is_mcq){
                    // the answer is not correct and units are correct
                    yellowLight.classList.add('activated');
                  //  alert('wrong answer, but correct units');
                  }
                  else {
                    // both answer and units were wrong
                    redLight.classList.add('activated');
                  }
                }

              }
            }, 1000);
        
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

    function removeAllLights(redLight, yellowLight, greenLight, blueLight){
      if(blueLight){
        blueLight.classList.remove('blinking');
        blueLight.classList.remove('activated');
      }

      redLight.classList.remove('activated');
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

  function getSelectedTrueAnswerIds(form) {
    const mcqOptions = form.querySelectorAll('.mcq-option-answer');
    const selectedAnswerIds = [];
  
    mcqOptions.forEach((option) => {
      const answerIdInput = option.querySelector('.answer_id');
      const answerInfoInput = option.querySelector('.answer_info');
  
      if (answerIdInput && answerInfoInput && answerInfoInput.value.charAt(0) === '1') {
        selectedAnswerIds.push(answerIdInput.value);
      }
    });
    //console.log(selectedAnswerIds);
    return selectedAnswerIds;
  }

function feedback_message(message){
  if(message != 'None'){
    alert(message);
  }
}





// Detecting latex in questions and displaying.
const questionContentPs = document.querySelectorAll(".question-content");
MathJax.typesetPromise().then(() => {

    questionContentPs.forEach((questionContentP) => {
        try{
            questionContentP.innerHTML = parseLatex(questionContentP.innerHTML);
            MathJax.typesetPromise();
        } catch(error){
           // console.log(error)
        }
    })
})

const prefacesInputs = document.querySelectorAll('.answer_preface');
if (prefacesInputs !=null){

  MathJax.typesetPromise().then(() => {

    prefacesInputs.forEach((preface) => {
        try{
            //console.log(preface.value);
            preface.value = MathJax.tex2chtml(preface.value).innerHTML;
            MathJax.typesetPromise();
            
        } catch(error){
           // console.log(error)
        }
    })
  })
}


function parseLatex(text) {
  const latexPattern = /#{(.*?)}#/g;
  const formattedText = text.replace(latexPattern, (_, latexCode) => {
      try {
          const mathJaxHTML = MathJax.tex2chtml(latexCode + '\\phantom{}');
          return mathJaxHTML.innerHTML;
      } catch (error) {
          //console.log(error);
          return ''; // Return an empty string if MathJax conversion fails.
      }
  });
  
  return formattedText;
}








//------------------------NOTES FEATURE and INFO----------------------//
const sideInfosIcons = document.querySelectorAll('.side-info-icon');
const sideInfox = document.querySelectorAll('.side-info-x');
const noteSection = document.querySelector('.note-section');
const noteEditBtn = noteSection.querySelector('.note-edit-btn');
const noteContent = noteSection.querySelector('.note-content');
const editHandlingSection = noteSection.querySelector('.edit-handling-section');
const noteTextArea = noteSection.querySelector('.note-textarea');
const saveNoteBtn = noteSection.querySelector('.save-note-btn');
const noteLastEdited = noteSection.querySelector('.note-last-edited');
const qrCodeBtn = noteSection.querySelector('.qr-code-btn');
const qrImage = document.getElementById("qrCodeImage");
var maintain_base_url = false
if(noteSection.classList.contains('dispatch-upload')){
 const clickEvent = new Event('click', {
    'bubbles': true, 
    'cancelable': true
});
//noteEditBtn.dispatchEvent(clickEvent);
// mainQuestionImageInput.click();
maintain_base_url = true
noteTextArea.style.display = 'block';
noteContent.style.display = 'none';
editHandlingSection.style.display = 'block';
noteSection.querySelectorAll('.add-delete-btns').forEach((btn)=>{
  btn.style.display = 'block';
})
noteEditBtn.style.display = 'none';

}

noteEditBtn.addEventListener('click', (event)=>{
  event.preventDefault();
  noteTextArea.style.display = 'block';
  noteContent.style.display = 'none';
  editHandlingSection.style.display = 'block';
  noteSection.querySelectorAll('.add-delete-btns').forEach((btn)=>{
    btn.style.display = 'block';
  })
  noteEditBtn.style.display = 'none';
})


sideInfox.forEach((Xbtn)=>{
  Xbtn.addEventListener('click', (event)=>{
    event.preventDefault();
    const sideDiv = Xbtn.closest('.side');
    sideDiv.querySelector('.side-info').classList.add('hide');
  })
})
var sideCounters = 0
sideInfosIcons.forEach((sideInfoIcon)=>{
sideInfoIcon.style.top = `${70 + 8*sideCounters}%`
sideCounters += 1;
sideInfoIcon.addEventListener('click', (event)=>{
  event.preventDefault();
  const sideDiv = sideInfoIcon.closest('.side');
  sideDiv.querySelector('.side-info').classList.remove('hide');
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
})
})

saveNoteBtn.addEventListener('click', ()=>{
  // implement the fetch here

  var imagePkArray = [];
  noteSection.querySelectorAll('.note-image-pk').forEach((pkField)=>{
    imagePkArray.push(pkField.value);
  })

  const formData = new FormData();
  const fileInputs = document.querySelectorAll('.uploaded_image');

  fileInputs.forEach((input) => {
      const file = input.files[0];
      if (file) {
          formData.append(input.name, file);
      }
  });
  formData.append('content', noteTextArea.value);
  formData.append('kept_images_pk', imagePkArray);
  const baseUrl = window.location.href.replace(/#$/, ''); // To strip of # at the end
  const fetchUrl = `${baseUrl}/save_note`;
  fetch(fetchUrl, {
    method: 'POST',
    body: formData,})
    .then(response => response.json())
    .then(data => {
        noteContent.innerHTML = data.md;
        noteLastEdited.innerHTML = `Last edited on ${data.last_edited}`;
        if (noteSection.classList.contains('dispatch-upload')){
          alert(`${data.message}\n Reload other device to see change.`)
        }
        
        noteEditBtn.style.display = 'block';
        noteTextArea.style.display = 'none';
        noteContent.style.display = 'block';
        editHandlingSection.style.display = 'none';
        noteSection.querySelectorAll('.add-delete-btns').forEach((btn)=>{
        btn.style.display = 'none';
        window.scrollTo({
          top: 0,
          behavior: 'smooth'
        });
        })
        })
    .catch(error => {
       console.error('Error:', error);
        });


})
//-----------------------IMAGE UPLOAD HANDLING---------------//
// Expanding image upload section
questionAddImgBtn.addEventListener('click', (event)=>{
  event.preventDefault();
  qrImage.style.display='none';
  if(questionAddImgBtn.classList.contains('open')){
      questionAddImgBtn.classList.remove('open');
      questionAddImgBtn.classList.add('closed');
      questionAddImgBtn.innerHTML = '-collapse-'
      questionImgUploadSection.style.display = 'block';
      questionImgUploadSection.scrollIntoView({behavior:'smooth'});
  }
  else{
      questionAddImgBtn.classList.remove('closed');
      questionAddImgBtn.classList.add('open');
      uploadedQuestionPreview.innerHTML = '';
      questionAddImgBtn.innerHTML = 'Upload Image';
      questionImgUploadSection.style.display = 'none'; 
  }
})


mainQuestionImageInput.addEventListener('change', function () {
  // Reads the uploaded image and renders on the page.
  uploadedQuestionPreview.innerHTML = '';
  for (const file of mainQuestionImageInput.files) {
      const img = document.createElement('img');
      img.src = URL.createObjectURL(file);
      img.style.maxWidth = '100%';
      img.style.maxHeight = '200px';
      img.style.borderRadius = '15px';
      img.classList.add('preview-image');
      uploadedQuestionPreview.appendChild(img);
  }
});

addQuestionImgBtn.addEventListener('click', (event)=>{
  event.preventDefault();
  if(mainQuestionImageInput.files.length === 0){
      alert('You must choose an image file.')
      return
  }

  try{
      const formatted_new_img = create_img_div(mainQuestionImageInput);
      mainQuestionImagePreview.appendChild(formatted_new_img);
      question_img_counter += 1;
      questionAddImgBtn.classList.remove('closed');
      questionAddImgBtn.classList.add('open');
      uploadedQuestionPreview.innerHTML = '';
      questionAddImgBtn.innerHTML = 'Upload Image';
      questionImgUploadSection.style.display = 'none'; 
  }
  catch(error){
      alert('Make sure you entered a label for the image and selected an image file.')
  }
  


})

// Deleting an uploaded image
mainQuestionImagePreview.addEventListener('click', (event)=>{
  event.preventDefault();
  target = event.target
  if(target.classList.contains('img-delete')){
      mainQuestionImagePreview.removeChild(target.parentNode.parentNode);
  }
})

function create_img_div(img_input_field){
  var imgDiv = document.createElement('div');
  imgDiv.className = 'question-image';
  imgDiv.innerHTML = `
  <br/>
  <div class="formatted-answer-option"></div>
  <div class="add-delete-btns">
      <button  type="button" class="btn btn-danger img-delete exempt">delete</button>
  </div>
`;
  var formattedImgDiv = imgDiv.querySelector('.formatted-answer-option');
  formattedImgDiv.appendChild(uploadedQuestionPreview.cloneNode(true));
  const image_input_field_clone = img_input_field.cloneNode(true);
  image_input_field_clone.name = `question_image_file_${question_img_counter}`;
  image_input_field_clone.style.display = 'none';
  image_input_field_clone.classList.add('uploaded_image');
  formattedImgDiv.appendChild(image_input_field_clone);
  uploadedQuestionPreview.innerHTML = '';
  img_input_field.value = '';

  return imgDiv;
}
qrCodeBtn.addEventListener('click', ()=>{
  showQRCode();
})

function showQRCode() {
  const temp_note = document.querySelector('.note-textarea').value;
  const imgElement = document.getElementById("qrCodeImage");
  
  // Construct the URL based on your Django URL pattern. Replace with the correct variable if not `main_question_id`.
  const baseUrl = window.location.href.replace(/#$/, '');

  fetch(`${baseUrl}/generate_note_qr`, {
    method: 'POST',
    headers: { 'X-CSRFToken': getCookie('csrftoken') },
    body: JSON.stringify({
            temp_note: temp_note,
            base_link: baseUrl,
            same_url: maintain_base_url   
    })
  })
  .then(response => response.blob())
  .then(blob => {
      const imageUrl = URL.createObjectURL(blob);
      imgElement.src = imageUrl;
      imgElement.style.display = "block";
  })
  .catch(error => {
      console.error("Error fetching the QR Code:", error);
  });
}


});

