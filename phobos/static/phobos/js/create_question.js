
document.addEventListener('DOMContentLoaded', () => {

    const expressionBtn = document.querySelector('#expression-btn');
    const answerFieldsDiv = document.querySelector('.answer-fields');
    const mcqAnswersDiv = document.querySelector('.mcq-answers');
    const form = document.querySelector('#question-form');
    let currentAction = form.getAttribute('action');
    const mcqBtn = document.querySelector('#mcq-btn');
    const mcqOptionBtnsDiv = mcqAnswersDiv.querySelector('.mcq-options-button');
    const inputedMcqAnswersDiv = document.querySelector('.inputed-mcq-answers');
    const imgLabelInputField = document.querySelector('.image-label-input-field');
    const questionAddImgBtn = document.querySelector('.main-question-add-image-btn');
    const questionImgUploadSection = document.querySelector('.question-image-upload-section');
    const uploadedQuestionPreview = document.querySelector('.uploaded-question-preview');
    var num_mcq_options_counter = 2;
    var num_true_counter = 0;
    var option_counter = 0;
    var question_img_counter = 0;
    const varSymbolsArray = [];

    const addQuestionImgBtn = document.querySelector('.question-image-add');
    const addMcqOptionBtn = document.querySelector('.mcq-add');
    
    const mcqInputDiv = document.querySelector('.mcq-input-div');
    const mcqInputField = mcqInputDiv.querySelector('.mcq-input-field');
    const mcqImagePreview = document.querySelector('.mcq-image-preview');
    const imageUploadInput = document.querySelector('.image-upload-input-field');
    const floatBtn = document.querySelector('#float-btn');
    const latexBtn = document.querySelector('#latex-btn');
    const frBtn = document.querySelector('#fr-btn');
    const surveyBtn = document.querySelector('#survey-btn');
    latexBtn.style.display = 'none';
    const formattedAnswerDiv = document.querySelector('#structural-formatted-answer');
    const screen = document.querySelector('#screen'); 
    const calculatorDiv = document.querySelector('.calculator');
    calculatorDiv.style.display = 'none';
    let mode = '';

    const mainQuestionImageInput = document.querySelector('.main-question-image-input');
    const mainQuestionImagePreview = document.querySelector('.main-question-image-preview');
  

/*-----------------------------------------SURVEY QUESTION-----------------------------------*/
    surveyBtn.addEventListener('click', (event)=> {
        event.preventDefault();
        mode = 's-answer';
        // NOT A HIGH PRIORITY FOR NOW. TO BE IMPLEMENTED LATER
    })

 /*------------------------------------------MCQ QUESTION --------------------------------- */
 

 imageUploadInput.addEventListener('change', ()=>{
    // Reads the uploaded image and renders on the page.
    // THERE is another way to do this at the bottom of this file which might be better
    // Ctrl + F and seatch 'image and renders' on page.
    const reader = new FileReader();
    const imageFile = imageUploadInput.files[0];
    reader.onload = function(event) {
        const imageElement = document.createElement('img');
        imageElement.src = event.target.result;
        imageElement.style.maxWidth = '100%';
        imageElement.style.maxHeight = '200px';
        imageElement.style.borderRadius = '15px';
        //console.log(imagePreview.src);
        
        mcqImagePreview.style.display = 'block';
        mcqImagePreview.innerHTML = '';
        mcqImagePreview.appendChild(imageElement);
    };
    if(imageFile){
        reader.readAsDataURL(imageFile);
    }
})

    mcqBtn.addEventListener('click', (event)=>{
    // If the instructor chooses mcq as the answer option.
    event.preventDefault();
        inputedMcqAnswersDiv.style.display = 'block';
        mcqImagePreview.style.display = 'block';
        mode = 'm-answer'
        num_mcq_options_counter = 0; // TODO: change this in case you want store the already inputed mcqs when the user 
                                    // changes answer type options. For example he may click on expression then come back to mcq.
        formattedAnswerDiv.style.display = 'none';
        calculatorDiv.style.display = 'none';
        mcqOptionBtnsDiv.style.display = 'block';
        // Append '/3' at the end of the URL
        const newAction = currentAction + '/3';
        // Update the form's action attribute
        form.setAttribute('action', newAction);
        

    });
    
    mcqOptionBtnsDiv.addEventListener('click', (event)=> {
        event.preventDefault();
        // Selecting different MCQ modes.
        mcqInputDiv.style.display = 'block';
        switch (event.target.id) {
            case 'mcq-expression-btn':
                imageUploadInput.style.display ='none';
                mcqImagePreview.style.display = 'none';
                mcqInputField.value = '';
                mcqInputField.placeholder = 'Enter expression and click add';
                mcqInputField.setAttribute('data-answer-type', 'e-answer');
                break;
            case 'mcq-float-btn':
                imageUploadInput.style.display ='none';
                mcqImagePreview.style.display = 'none';
                mcqInputField.value = '';
                mcqInputField.placeholder = 'Enter float and click add';
                mcqInputField.setAttribute('data-answer-type', 'f-answer');
                break;
            case 'mcq-text-btn':
                imageUploadInput.style.display ='none';
                mcqImagePreview.style.display = 'none';
                mcqInputField.value = '';
                mcqInputField.placeholder = 'Enter text and click add';
                mcqInputField.setAttribute('data-answer-type', 't-answer');
                break;
            case 'mcq-latex-btn':
                imageUploadInput.style.display ='none';
                mcqImagePreview.style.display = 'none';
                mcqInputField.value = '';
                mcqInputField.placeholder = 'Enter latex and click add';
                mcqInputField.setAttribute('data-answer-type', 'l-answer');
                break;
            case 'mcq-image-btn':
                mcqInputField.value = '';
                mcqInputField.placeholder = 'Enter image label and click add';
                mcqInputField.setAttribute('data-answer-type', 'i-answer');
                imageUploadInput.style.display ='block';
                mcqImagePreview.style.display = 'block';
            default:
                // Nothing yet
        }
    })

    
    addMcqOptionBtn.addEventListener('click', (event)=>{
        event.preventDefault();
        // Adding an mcq option after filling the input field.
        // This may look small but it's the most dense function in this file
        // Checkout create_inputed_mcq_div() to see what I mean.
        if (mcqInputField.value === null || mcqInputField.value ==='') {
            alert('Cannot create an empty mcq option.')
            
        }
        else{
            try{
                const validText = validateText(mcqInputField.value, varSymbolsArray);
                if(!validText){
                    alert('Undefined symbol(s) in variable expression(s)');
                    return;
                }
                const formatted_new_answer = create_inputed_mcq_div(mcqInputField, mcqInputField.dataset.answerType);
                inputedMcqAnswersDiv.appendChild(formatted_new_answer);
                mcqInputField.value = '';
                option_counter += 1;
            }
            catch(error){
                alert('Make sure you enter the correct format of the answer type you selected.')
            }
            
        }


    })

    inputedMcqAnswersDiv.addEventListener('click', (event)=>{
        event.preventDefault();
        // Here adding the ability to change the status of an mcq option as true or false
        // Also, there's a delete button.
        target = event.target
        if(target.classList.contains('mcq-false')){
            // changing an mcq option from false to true.
            target.classList.remove('mcq-false','btn-warning');
            target.classList.add('mcq-true', 'btn-info');
            target.innerHTML = 'True';
            num_true_counter += 1;
            const answer_info_input = target.parentNode.parentNode.querySelector('.answer_info');
            answer_info_input.value = rep(answer_info_input.value, 0, '1');
        } else if(target.classList.contains('mcq-true')){
            // changing an mcq option from true to false.
            target.classList.add('mcq-false','btn-warning');
            target.classList.remove('mcq-true', 'btn-info');
            target.innerHTML = 'False'; 
            num_true_counter -= 1;    
            const answer_info_input = target.parentNode.parentNode.querySelector('.answer_info');
            answer_info_input.value = rep(answer_info_input.value, 0, '0');
        } else if (target.classList.contains('mcq-delete')){
            // deleting an mcq option.
            num_mcq_options_counter -= 1;
            if (target.classList.contains('mcq-true')){
                num_true_counter -= 1;
            }
            inputedMcqAnswersDiv.removeChild(target.parentNode.parentNode.parentNode);//TODO: Can probably make this something better.
        }
    })








    /*------------------------------------------STRUCTURAL QUESTION --------------------------------- */
    // latexAnswerDiv is never used but just keeping it here.
    const latexAnswerDiv = `
    <div class="l-answer"><br/>
    <label>Latex Answer:</label>
        <input style="width: 100%; box-sizing: border-box;" class="question-input-field" placeholder="Enter LaTex" type="text" class="latex-answer-input" name="answer"/>
        </div>
    `
    // Free response button selected.
    frBtn.addEventListener('click', (event)=>{
        event.preventDefault();
        mode = 'fr-answer';  
        inputedMcqAnswersDiv.style.display = 'none';
        formattedAnswerDiv.innerHTML = 'Free response mode selected.'
        formattedAnswerDiv.style.display = 'block';
        mcqOptionBtnsDiv.style.display = 'none';
        mcqInputDiv.style.display = 'none';
        mcqImagePreview.style.display = 'none';
        calculatorDiv.style.display = 'none';
        answerFieldsDiv.innerHTML = '';
        
        formattedAnswerDiv.scrollIntoView({behavior: 'smooth'});
        // Append '/4' at the end of the URL
        const newAction = currentAction + '/4';
        // Update the form's action attribute
        form.setAttribute('action', newAction);      
    })

    // Expression answer button selected.
    expressionBtn.addEventListener('click', (event)=> {
        event.preventDefault();
        mode = 'e-answer';
        inputedMcqAnswersDiv.style.display = 'none';
        formattedAnswerDiv.style.display = 'block';
        mcqOptionBtnsDiv.style.display = 'none';
        mcqInputDiv.style.display = 'none';
        mcqImagePreview.style.display = 'none';
        calculatorDiv.style.display = 'block';
        answerFieldsDiv.innerHTML = '';
        screen.value = ''
        screen.placeholder = 'Algebraic expression';
        formattedAnswerDiv.innerHTML = ''

        answerFieldsDiv.scrollIntoView({ behavior: 'smooth' });
    
        // Append '/0' at the end of the URL
        const newAction = currentAction + '/0';
        // Update the form's action attribute
        form.setAttribute('action', newAction);

    });

    // Float button selected.
    floatBtn.addEventListener('click', function(event) { 
        event.preventDefault();
        mode = 'f-answer';
        inputedMcqAnswersDiv.style.display = 'none';
        formattedAnswerDiv.style.display = 'block';
        mcqOptionBtnsDiv.style.display = 'none';
        mcqInputDiv.style.display = 'none';
        mcqImagePreview.style.display = 'none';
        calculatorDiv.style.display = 'block';
        answerFieldsDiv.innerHTML = '';
        screen.value = ''
        screen.placeholder = 'Enter real number';
        formattedAnswerDiv.innerHTML = ''

        answerFieldsDiv.scrollIntoView({ behavior: 'smooth' });
        // Append '/1' at the end of the URL
        const newAction = currentAction + '/1';
        // Update the form's action attribute
        form.setAttribute('action', newAction);
    });

    // Latex button selected. Probably never used.
    latexBtn.addEventListener('click', (event)=> {
        event.preventDefault();
        mode = 'l-answer'
        inputedMcqAnswersDiv.style.display = 'none';
        formattedAnswerDiv.style.display = 'block';
        mcqOptionBtnsDiv.style.display = 'none';
        mcqInputDiv.style.display = 'none';
        mcqImagePreview.style.display = 'none';
        calculatorDiv.style.display = 'none';
        screen.value = ''
        formattedAnswerDiv.innerHTML = ''
        answerFieldsDiv.innerHTML = latexAnswerDiv;
        answerFieldsDiv.scrollIntoView({ behavior: 'smooth' });
    
        // Append '/2' at the end of the URL
        const newAction = currentAction + '/2';
        // Update the form's action attribute
        form.setAttribute('action', newAction);



        // Adding event listener to the input field.
        const latexInput = answerFieldsDiv.querySelector('input');
        latexInput.addEventListener('input', ()=>{
            var answerFieldDiv = answerFieldsDiv.querySelector('div');
            var latexInputField = answerFieldDiv.querySelector('input');
            const userInputLatex = latexInputField.value;
           
            MathJax.typesetPromise().then(() => {
                try{
                    const formattedAnswer = MathJax.tex2chtml(userInputLatex + '\\phantom{}');
                    formattedAnswerDiv.innerHTML = '';
                    formattedAnswerDiv.appendChild(formattedAnswer);
                    MathJax.typesetPromise();
                } catch(error){
                    //console.log(error);
                }

              });


        })
    });
    // Here, each time the value of answer input screen changes,
    // we use mathjax to display the updated content.
    screen.addEventListener('input', ()=> {
        if(screen.value.length != 0){

            MathJax.typesetPromise().then(() => {
                try {
    
                const userInputNode = math.simplify(processString(screen.value));
                var userInputLatex = userInputNode.toTex();
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
    form.addEventListener('submit', (event) => {
        // Make sure question text is valid
        const questionTextArea = form.querySelector('#question-textarea');
        if (questionTextArea.value.length <= 5){
            event.preventDefault();
            alert('A question cannot be this short!');
            return;
        }
        const valid_textarea = validateText(questionTextArea.value, varSymbolsArray);
        if (!valid_textarea){
            event.preventDefault();
            alert('The question text has undefined symbol(s) in variable expression(s)');
            return;
        }
        const selected_topic = checkTopicAndSubtopic();
        if (!selected_topic){
            event.preventDefault();
            alert("Please select both a topic and a subtopic.");
            return;
        }
        if (mode==='e-answer'){
            try{
                const userInputNode = math.simplify(processString(screen.value));
                var userInputString = userInputNode.toString();
                // The following is in case we don't want to change the domain of the algebraic expression
                // for example, if we don't want (x+1)(x-1)/(x-1) to simplify to just (x+1)
                //var userInputString = math.simplify(userInputNode, {}, {context: math.simplify.realContext}).toString()
                screen.value = userInputString;

            }catch {
                event.preventDefault();
                alert('Expression in answer not valid algebraic expression');
                return;
            }

        }
        else if(
            mode==='f-answer'
        ) {
            try{
                const userInputNode = math.simplify(processString(screen.value));
                var userInputString = userInputNode.evaluate();
                if(typeof(userInputString) != 'number'){

                    event.preventDefault();
                    alert('You selected float mode but the answer you provided is not a float');
                    return;
                }
                screen.value = userInputString;
            }catch {
                if(!validateText(screen.value, varSymbolsArray, isFloat=true)){

                    event.preventDefault();
                    alert('You selected float mode but the answer you provided is not a float');
                    return;
                 }
            }
            
            
        } else if (mode=='m-answer'){
            if(num_mcq_options_counter < 2){
                event.preventDefault();
                alert('The number of options for an MCQ must be at least 2.');
            }
            if(num_true_counter < 1){
                event.preventDefault();
                alert('Must select at least one MCQ answer as correct.');
            }
        }
        // Now the form will be submitted
    });






function create_inputed_mcq_div(input_field, answer_type) {
    var answer_value = input_field.value
    var inputedMcqDiv = document.createElement('div'); // to be appended to .inputed-mcq-answers.
    num_mcq_options_counter += 1;
    var answer_info_encoding = '000' // First character for True or False, second for question type, and third for question_number 
    // The following is a blue print of the information stored about an mcq-option.
    // One of the hidden inputs should store the string value of the answer, as well as the type of answer it is..
    // The other hidden input will store the reference question.i.e 0 = 'main', 1 = 'a', 2 = 'b', 4 = 'c' etc. 
    //     so 0 may mean it is an mcq option for the main question. while 'b' means it is sub question.
   // May add an edit button later, but I don't think it is useful.
    var formatted_answer = '';
    switch (answer_type) {
        case 'f-answer':
            // TODO: the float may have variables, so improve the condition below by testing
            // whether the string contains variables or not.
            try{
                display_value = answer_value;
                answer_value = math.simplify(processString(answer_value)).evaluate();
                if(typeof(answer_value) != 'number'){
                    num_mcq_options_counter -= 1
                    alert('You selected float mode but the answer you provided is not a float');
                    return;
                }
                
            }catch {
                if(validateText(answer_value, varSymbolsArray, isFloat=true)){
                    display_value = answer_value;
                }else{
                    num_mcq_options_counter -= 1
                    alert('You selected float mode but the answer you provided is not a float');
                    return;
                }
                
            }
            answer_info_encoding = rep(answer_info_encoding, 1, '1');
            break;
        case 't-answer':
            display_value = answer_value;
            answer_info_encoding = rep(answer_info_encoding, 1, '3');
            break;
        case 'l-answer':
            display_value = answer_value; // Actually doesn't do anything because we don't use Latex as a direct answer yet.
            answer_info_encoding = rep(answer_info_encoding, 1, '2');
            break;
        case 'e-answer':
            try{
                answer_value = math.simplify(processString(answer_value)).toString();
                display_value = answer_value;
            }
            catch{
                num_mcq_options_counter -= 1
                alert('Expression(s) not valid algebraic expression');   
                return;
            }
            answer_info_encoding = rep(answer_info_encoding, 1, '0');
            break;
        case 'i-answer':
            display_value = answer_value;
            answer_value = 'image_' + answer_value; 
            answer_info_encoding = rep(answer_info_encoding, 1, '7');
        default:
            //
    }
    MathJax.typesetPromise().then(() => {
        var userInputLatex = '';
        try {
            if (answer_type==='l-answer'){// if latex-answer or text-answer
                userInputLatex = answer_value;
                formatted_answer = MathJax.tex2chtml(userInputLatex + '\\phantom{}');
            } else if(answer_type==='t-answer'){
                userInputLatex = answer_value;
                formatted_answer = document.createElement('p');
                formatted_answer.innerHTML = userInputLatex;
            }
            else {
                try{
                    const userInputNode = math.simplify(processString(display_value));
                    userInputLatex = userInputNode.toTex();
                    formatted_answer = MathJax.tex2chtml(userInputLatex + '\\phantom{}');
                }catch{
                    formatted_answer = document.createElement('p');
                    formatted_answer.innerHTML = display_value;
                }
                
            }
            

            // Now that the formatted_answer is ready, create the necessary HTML structure
            var mcqAnswerDiv = document.createElement('div');
            mcqAnswerDiv.className = 'inputed-mcq-answer';
            if (answer_type != 'i-answer'){
                mcqAnswerDiv.innerHTML = `
                <br/>
                <div class="formatted-answer"></div>
                <input value="${answer_value}" type="hidden" name="answer_value_${option_counter}"/>
                <input value="${answer_info_encoding}" type="hidden" class="answer_info" name="answer_info_${option_counter}"/>
                <div class="add-delete-btns">
                    <button type="button" class="btn btn-warning mcq-status mcq-false exempt">False</button>
                    <button  type="button" class="btn btn-danger mcq-delete exempt">delete</button>
                </div>
            `;
             }else {
                mcqAnswerDiv.innerHTML = `
                <br/>
                <div class="formatted-answer"></div>
                <input value="${display_value}" type="hidden" name="image_label_${option_counter}"/>
                <input value="${answer_info_encoding}" type="hidden" class="answer_info" name="answer_info_${option_counter}"/>
                <div class="add-delete-btns">
                    <button type="button" class="btn btn-warning mcq-status mcq-false exempt">False</button>
                    <button  type="button" class="btn btn-danger mcq-delete exempt">delete</button>
                </div>
            `;
            
             }
           
            // Append the formatted_answer element as a child
            var formattedAnswerDiv = mcqAnswerDiv.querySelector('.formatted-answer');
            formattedAnswerDiv.appendChild(formatted_answer);
            if (answer_type === 'i-answer'){
                formattedAnswerDiv.appendChild(mcqImagePreview.cloneNode(true));
                const image_input_field_clone = imageUploadInput.cloneNode(true);
                image_input_field_clone.name = `answer_value_${option_counter}`;
                image_input_field_clone.style.display = 'none';
                formattedAnswerDiv.appendChild(image_input_field_clone);
                imageUploadInput.value = '';
                mcqImagePreview.innerHTML = '';
            }
            formattedAnswerDiv.scrollIntoView({behavior:'smooth'});

            // Append mcqAnswerDiv to inputedMcqDiv
            inputedMcqDiv.appendChild(mcqAnswerDiv);
            MathJax.typesetPromise();
        } catch (error) {
            console.log(error);
        }
    });


    return inputedMcqDiv;
}





//------------------------------------IMAGE UPLOAD HANDLING FOR MAIN QUESTION-------------------
// Expanding image upload section
questionAddImgBtn.addEventListener('click', (event)=>{
    event.preventDefault();
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
    if (imgLabelInputField.value === null || imgLabelInputField.value ==='') {
        alert('You must enter a label for the image.')
        
    }
    else{
        try{
            const formatted_new_img = create_img_div(mainQuestionImageInput, imgLabelInputField.value);
            mainQuestionImagePreview.appendChild(formatted_new_img);
            imgLabelInputField.value = '';
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
        
    }


})
// Deleting an uploaded image
mainQuestionImagePreview.addEventListener('click', (event)=>{
    target = event.target
    if(target.classList.contains('img-delete')){
        mainQuestionImagePreview.removeChild(target.parentNode.parentNode);
    }
})

function create_img_div(img_input_field, img_label){
    var imgDiv = document.createElement('div');
    var imgLabel = document.createElement('p');
    imgLabel.innerHTML = img_label;
    imgDiv.className = 'question-image';
    imgDiv.innerHTML = `
    <br/>
    <div class="formatted-answer"></div>
    <input value="${img_label}" type="hidden" name="question_image_label_${question_img_counter}"/>
    <div class="add-delete-btns">
        <button  type="button" class="btn btn-danger img-delete exempt">delete</button>
    </div>
`;
    var formattedImgDiv = imgDiv.querySelector('.formatted-answer');
    formattedImgDiv.appendChild(imgLabel);
    formattedImgDiv.appendChild(uploadedQuestionPreview.cloneNode(true));
    const image_input_field_clone = img_input_field.cloneNode(true);
    image_input_field_clone.name = `question_image_file_${question_img_counter}`;
    image_input_field_clone.style.display = 'none';
    formattedImgDiv.appendChild(image_input_field_clone);
    uploadedQuestionPreview.innerHTML = '';
    img_input_field.value = '';

    return imgDiv;
}

/*------------------------------UTILITY FUNCTIONS ----------------------------*/
function rep(str, index, char) {
    str = setCharAt(str,index,char);
    return str
}

function setCharAt(str,index,chr) {
    if(index > str.length-1) return str;
    return str.substring(0,index) + chr + str.substring(index+1);
}

function checkTopicAndSubtopic() {
    var topicSelect = document.getElementById("topicSelect");
    var subTopicSelect = document.getElementById("subTopicSelect");
    
    if (topicSelect.value === "" || subTopicSelect.value === "") {

      return false; // Prevent form submission
    }
    
    // If both topic and subtopic are selected, you can submit the form
    return true;
  }

  function validateText(text, array, isFloat=false) {
    // Check if "{...}" is present in the text and verifies there are non-numeric strings in {}
    // in the text are in the list of variables

    //  returns False if string in {} is non-numerice and not in the list of variables
    // returns true otherwise.

    const match = text.match(/@\{(.+?)\}@/);
    if(isFloat){
        if(text.startsWith("@{") && text.endsWith("}@")){
            // we use - 4 because "@{" and "}@" count as four characters
            if(text.length - 4 != match[1].length){
                return false
            } 
        }else {
            return false
        }

        const contentWithinBraces = match[1];
        const contentArray = extractSymbols(contentWithinBraces);
        if (!contentArray){
          return false;
        }
        // Check if all non-numeric strings in contentArray are in the array
        for (const item of contentArray) {
          const trimmedItem = item.trim();
          if (!isNaN(trimmedItem) || array.includes(trimmedItem)) {
            // Numeric or found in the array
            continue;
          } else {
            // Non-numeric and not found in the array
            return false;
          }
        }
        
        return true; // All non-numeric strings are found in the array
    }
  
    else {
        if (match) {
      const contentWithinBraces = match[1];
      const contentArray = extractSymbols(contentWithinBraces);
      if (!contentArray){
        return false;
      }
      // Check if all non-numeric strings in contentArray are in the array
      for (const item of contentArray) {
        const trimmedItem = item.trim();
        if (!isNaN(trimmedItem) || array.includes(trimmedItem)) {
          // Numeric or found in the array
          continue;
        } else {
          // Non-numeric and not found in the array
          return false;
        }
      }
      
      return true; // All non-numeric strings are found in the array
    }
  
    return true; // No "{...}" found in the text
  }
}
  

  function extractSymbols(expr) {
    // Insert space between combined characters. For example (0.28*a) becomes (0.28 a)
    //const expression = expr.replace(/ /g, '');
    var expression;
    try {
        expression = math.simplify(expr).toString();
    } catch {
        alert('Algebraic expression(s) in the variable expression(s) @{..}@ invalid');
        return false;
    }
    const symbols = [];
    var char;
    var run = false;
    var sub_index;
    for (let index = 0; index < expression.length; index++) {
      char = expression.charAt(index);
      
        if (/[a-zA-Z]/.test(char) && expression.charAt(index-1) != '-') {
        run = true
        sub_index = index + 1
        while(run && sub_index <= expression.length){
            if((sub_index === expression.length)){
                symbols.push(expression.slice(index, sub_index));
                run = false; //useless here though.
            }
            else if(expression.charAt(sub_index) === ' ' || expression.charAt(sub_index) === '(' ||
            expression.charAt(sub_index) === ')'){

                symbols.push(expression.slice(index, sub_index));
                run = false;
            }
            sub_index  += 1;
        }
    }
}
    return symbols
  }






  //-----------------------------HANDLING VARIABLES---------------------------------------//

  
  const addVarBtn = document.querySelector('.var-btn');
  const varInfoDiv = document.querySelector('.var-info-div');
  const createdVarsDiv = document.querySelector('.created-vars');

  var symbol = '';
  var enteredDomain = '';
  varInfoDiv.style.display = 'none';
  var state = 'closed';
  addVarBtn.addEventListener('click', (event)=>{
      event.preventDefault();
      if(state==='closed'){
          state = 'open';
          addVarBtn.innerHTML ='v-';
          varInfoDiv.style.display = 'block';
      }
      else if(state==='open'){
          state ='closed';
          addVarBtn.innerHTML = 'v+';
          varInfoDiv.style.display = 'none';
      }
  })
  
  varInfoDiv.addEventListener('click', (event)=>{
      event.preventDefault();
      if(event.target.classList.contains('btn-create-var')){
          const varSymbolField = varInfoDiv.querySelector('.var-symbol');
          const varDomainField = varInfoDiv.querySelector('.var-domain');
          symbol = varSymbolField.value;
          // Checking whether it's a valid symbol
          if (symbol.length === 0 ){
              alert('You must enter a symbol');
              return;
          } else if(varSymbolsArray.includes(symbol)){
            alert('Symbol already in used');
            return;
          }else if(symbol.length === 1)
          {
            if(/[aijk]/.test(symbol)){
                alert('Unauthorized symbol due to vectors, trigonometric, or complex numbers issues (5i -2j + k, a +bi, asin, arctan, arccos, etc)');
                return;
            }
          }
          else if ((symbol.length > 3) || (symbol.length === 2) || (/^[a-zA-Z]$/.test(symbol.charAt(0)) === false) || 
          ((symbol.charAt(1) != '_') && (symbol.length===3))){
              alert('Invalid symbol');
              return;
          }
          // Checking whether domain entered is valid
          enteredDomain = varDomainField.value;
          var parsedDomain = parseDomainInput(enteredDomain);
          if(parsedDomain.length === 0){
              alert('Invalid domain');
              return;
          }
        
          // passed all the tests
          varSymbolsArray.push(symbol);
          const newVarDiv = document.createElement('div');
          const newVarBtn = document.createElement('button');
          newVarBtn.type = 'button';
          newVarBtn.classList.add('btn', 'btn-warning'); // Separate the classes
          
          newVarBtn.innerHTML = symbol;
          newVarDiv.appendChild(newVarBtn);
          newVarDiv.classList.add('variable');
          newVarDiv.setAttribute('data-symbol', symbol);
          for (let i = 0; i < parsedDomain.length; i++) {
              const domainLbHiddenInput = document.createElement('input');
              domainLbHiddenInput.type = 'hidden';
              domainLbHiddenInput.name = `domain_lb_${symbol}_${i}`
              domainLbHiddenInput.value = parsedDomain[i].lower
              
              const domainUbHiddenInput = document.createElement('input');
              domainUbHiddenInput.type = 'hidden';
              domainUbHiddenInput.name = `domain_ub_${symbol}_${i}`
              domainUbHiddenInput.value = parsedDomain[i].upper

              newVarBtn.appendChild(domainLbHiddenInput);
              newVarBtn.appendChild(domainUbHiddenInput);
          }
          // TODO: add the hidden input fields.
          createdVarsDiv.appendChild(newVarDiv);
          createdVarsDiv.scrollIntoView({behavior:"smooth"});
          varInfoDiv.style.display = 'none';
          varSymbolField.value = '';
          varDomainField.value = '';

          state ='closed';
          addVarBtn.innerHTML = 'v+';

      }

  })


  function parseDomainInput(input) {
    const boundsArray = [];
    const groups = input.match(/\[(.*?)\]/g); // Match text within parentheses

    if (groups) {
        groups.forEach(group => {
            const bounds = group.slice(1, -1).split(','); // Remove parentheses and split by comma
            if (bounds.length === 2) {
                const lowerBound = parseFloat(bounds[0]);
                const upperBound = parseFloat(bounds[1]);
                if (!isNaN(lowerBound) && !isNaN(upperBound)) {
                    boundsArray.push({ lower: lowerBound, upper: upperBound });
                }
            }
        });
    }

    return boundsArray;
}
});


  
