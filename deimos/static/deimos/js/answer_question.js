document.addEventListener('DOMContentLoaded', ()=> {
    const forms = document.querySelectorAll('.question-form');
    const validateAnswerActionURL = extractQuestionPath(window.location.href) + '/validate_answer';
    const screen = document.querySelector('#screen'); 
    var formattedAnswerDiv;
   


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
        console.log(prevSubmitBtn);

        previousForm.querySelector('.inputed_answer_structural').value = screen.value;
        previousForm.querySelector('.inputed_units_structural').value = calculatorDiv.querySelector('.units-screen').value;
      }
      
      form.appendChild(calculatorDiv)
      calculatorDiv.classList.remove('hide');
      calculatorDiv.querySelector('.preface-content').innerHTML = form.querySelector('.answer_preface').value
      screen.value = form.querySelector('.inputed_answer_structural').value;
      if(form.querySelector('.show_unit').value ==='yes'){
        calculatorDiv.querySelector('.units-screen').value = form.querySelector('.inputed_units_structural').value
        calculatorDiv.querySelector('.units-section').style.display='block';
      }else{
        calculatorDiv.querySelector('.units-section').style.display='none';
      }
      screen.dataset.changedPart = 'true';


      return;  
    }
    const yellowLight = form.querySelector('.yellow-light');
    const greenLight = form.querySelector('.green-light');
    const redLight = form.querySelector('.red-light');
    
    // For now, yellow light represents to many attempts
    if(!greenLight.classList.contains('activated') && !yellowLight.classList.contains('activated')){
      // Checking whether the submitted answer is valid
      const questionType = form.querySelector('.question-type');
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
    if (question_type.startsWith('structural')){
       
        fetch(`/${validateAnswerActionURL}/${qid}`, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            body: JSON.stringify({
                    answer: answer_struct.toString(),
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
              feedback_message(result.feedback_data);
          });
    } else if( question_type ==='mcq'){
        // TODO make sure some mcqs are selected as true.
        fetch(`/${validateAnswerActionURL}/${qid}`, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            body: JSON.stringify({
                    answer: getSelectedTrueAnswerIds(form),
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
                    MathJax.typesetPromise();
                }

            } catch (error) {
                //console.log(error);
            }
        });
    });

}

displayLatex();



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
    function toggleLight(correct, too_many_attempts,redLight, yellowLight, greenLight) {
        // Make the yellow light blink as though the program was 'thinking';

          if (correct) {
            
            setTimeout(function () {
              // Code to execute after 1.6 seconds
              yellowLight.classList.remove('activated');
              yellowLight.classList.remove('blinking');
              greenLight.classList.add('activated');
            }, 1000);
        
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

function feedback_message(result){

  console.log(result);
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
           console.log(error)
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








//------------------------NOTES FEATURE----------------------//
const notePencil = document.querySelector('.note-pencil');
const noteSection = document.querySelector('.note-section');
const noteXBtn = noteSection.querySelector('#close-x-note');
const noteEditBtn = noteSection.querySelector('.note-edit-btn');
const noteContent = noteSection.querySelector('.note-content');
const editHandlingSection = noteSection.querySelector('.edit-handling-section');
const noteTextArea = noteSection.querySelector('.note-textarea');
const saveNoteBtn = noteSection.querySelector('.save-note-btn');
const noteLastEdited = noteSection.querySelector('.note-last-edited');
const qrCodeBtn = noteSection.querySelector('.qr-code-btn');
const qrImage = document.getElementById("qrCodeImage");

if(noteSection.classList.contains('dispatch-upload')){
 const clickEvent = new Event('click', {
    'bubbles': true, 
    'cancelable': true
});
console.log('auto upload')
//noteEditBtn.dispatchEvent(clickEvent);
// mainQuestionImageInput.click();
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

noteXBtn.addEventListener('click', (event)=>{
  event.preventDefault();
  noteSection.classList.add('hide');
})

notePencil.addEventListener('click', (event)=>{
  event.preventDefault();
  noteSection.classList.remove('hide');
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
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
        alert(data.message);
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
            base_link: baseUrl   
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

