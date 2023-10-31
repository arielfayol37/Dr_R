
document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('#question-form');
    const allQuestionBlocks = form.querySelector("#all-question-blocks");
    let currentAction = form.getAttribute('action');
    const varSymbolsArray = ['ò', 'ë', 'à', 'ê', 'ä', 'ï', 'ù', 'ô', 'ü', 'î', 'â', 'ö', 'ÿ', 'è', 'é', 'ç', 'û', 'β', 'я', 'α'];
    const screen = document.querySelector('#screen'); 
    const calculatorDiv = document.querySelector('.calculator');
    calculatorDiv.style.display = 'none';
    const createQuestionBtn = document.querySelector('.create-question-btn');
    var settingsPreviousValue = 1;
    const settingsSelect = document.querySelector('.settings-select');
    var initial_num_points = document.querySelector('.init-num-pts').value;

  
    var num_questions = 1;
    var part_num_questions = 1;
    
    var questionTypeDicts = {
    }

    allQuestionBlocks.appendChild(addQuestionBlock());
  

    // Here, each time the value of answer input screen changes,
    // we use mathjax to display the updated content.
    screen.addEventListener('input', ()=> {
        const formattedAnswerDiv = screen.closest('.question-block').querySelector('.structural-formatted-answer');
        if(screen.value.length >=1 && screen.value.length < 40){
            
            MathJax.typesetPromise().then(() => {
                try {
                if(screen.value.startsWith('@{') && screen.value.endsWith('}@')){
                    var processed = processString(screen.value.slice(2,-2))
                    var userInputNode = math.simplify(processed);
                    var parsedNode = math.parse(processed);
                }else{
                    var processed = processString(screen.value)
                    var userInputNode = math.simplify(processed);
                    var parsedNode = math.parse(processed);
                }
                var userInputLatex = parsedNode.toTex() + '\\quad = \\quad' + userInputNode.toTex();
                const formattedAnswer = MathJax.tex2chtml(userInputLatex + '\\phantom{}');
                
                formattedAnswerDiv.innerHTML = '';
                formattedAnswerDiv.appendChild(formattedAnswer);
                MathJax.typesetPromise();
                } catch (error) {
                   //console.log(error);
                }
                
                }); 
        }else {
            formattedAnswerDiv.innerHTML = '';
        }


    })
    form.addEventListener('submit', (event) => {
        event.preventDefault();
    });

    createQuestionBtn.addEventListener('click', (event)=>{
        event.preventDefault();
        // Create a click event and dispatch it on the answer-options of the
        // question block containing the screen so that the hidden answer input 
        // fields are filled.
        let clickEvent = new Event('click', {
            'bubbles': true,
            'cancelable': true
        });
        const lastQB = screen.closest('.question-block');
        if(lastQB != null){
            lastQB.querySelector('.answer-options').dispatchEvent(clickEvent);
        }


        // Dispatching event on settings select so that the last changes are updated
        const changeEvent = new Event('change', {
            'bubbles': true,
            'cancelable': true
        });
    
        settingsSelect.dispatchEvent(changeEvent);
        
        const questionBlocks = allQuestionBlocks.querySelectorAll('.question-block');
        for (let i = 0; i < questionBlocks.length; i++) {
        
            let okay = checkQuestionBlock(questionBlocks[i]);
            if (!okay) {
                alert(`Problem found on part ${String.fromCharCode(64 + i + 1)}`);
                return;  // Exit the loop
            }
        }

        var newAction = '';
        // After all the tests have passed. 
        // console.log(questionTypeDicts);
        for (let key in questionTypeDicts) {
            if (questionTypeDicts.hasOwnProperty(key)) {  // This check ensures that you only access direct properties of the object, not properties inherited from the prototype
                let value = questionTypeDicts[key];
                newAction = newAction + '$'+ `${key}` + `-${value}`
            }
        }
        newAction = currentAction + `/${newAction}`;
        // Now the form will be submitted after all the checks have passed.
        form.setAttribute('action', newAction);
        //console.log(newAction);
        form.submit();
    })










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
    // Takes a text and checks the presence of variable expressions.
    // If there are variable expressions, then it checks whether there are
    // undefined symbols(variables) within the expression. If all symbols are defined,
    // it returns true, otherwise false.

    // if isFloat, then it expecting a single variable expression because this function
    // is called if and only if the user selected float but what he entered is not float.
    // hence, it returns false if a variable expression is not detected but returns true
    // if one is detected and all the symbols within are defined. 


    // IMPORTANT: though the following may look similar to what has been done elsewhere
    // so do not just copy and paste.
    const trigFunctions = {
        'asin': 'ò', 'acos': 'ë', 'atan': 'à', 'arcsin': 'ê', 'arccos': 'ä',
        'arctan': 'ï', 'sinh': 'ù', 'cosh': 'ô', 'tanh': 'ü', 'sin': 'î', 'cos': 'â', 
        'tan': 'ö', 'log': 'ÿ', 'ln': 'è',
        'cosec': 'é', 'sec': 'ç', 'cot': 'û', 'sqrt':'β', 'pi': 'я', '√':'α'
    };
    // console.log(`text to be validated before encoding: ${text}`)
    text = encode(processString(text), trigFunctions);
    // console.log(`text to be validated after encoding: ${text}`)
    if (isFloat) {

        const match = text.match(/@\{(.+?)\}@/);
        if (text.startsWith("@{") && text.endsWith("}@") && match && match[1].length >= 1) {
            const contentWithinBraces = match[1];
            // console.log(`extracted expression within the braces: ${contentWithinBraces}`);
           
            const contentArray = extractSymbols(contentWithinBraces);

            // console.log(`extracted symbols from expression: ${contentArray}`)
            if (contentArray.length==0) {
                alert('There is no variable in the entered expression.');
                return false;
            }
            //console.log(contentArray);
            for (const item of contentArray) {
                const trimmedItem = item.trim();
                if (isNaN(trimmedItem) && !array.includes(trimmedItem)) {
                    alert(`${trimmedItem} is not defined`);
                    return false;
                }
            }
            return true;
        }
        return false; 
    } else {
        const matches = text.match(/@\{(.+?)\}@/g);
        if (matches) {
            for (const m of matches) {
                const contentWithinBraces = m.slice(2, -2); // Extract content without using another regex
                // console.log(`extracted expression within the braces: ${contentWithinBraces}`);
                const contentArray = extractSymbols(contentWithinBraces);
                // console.log(`extracted symbols from expression: ${contentArray}`)
                if (contentArray.length == 0) {
                    alert('There is no variable in the entered expression.');
                    return false;
                }
                for (const item of contentArray) {
                    const trimmedItem = item.trim();
                    if (isNaN(trimmedItem) && !array.includes(trimmedItem)) {
                        alert(`${trimmedItem} is not defined`);
                        return false;
                    }
                }
            }
        }
        return true;
    }
} 

  

  function extractSymbols(expr) {
    // Insert space between combined characters. For example (0.28*a) becomes (0.28 a)
    //const expression = expr.replace(/ /g, '');
    var expression;
    try {
        expression = math.simplify(expr).toString();
    } catch {
        console.log(expr)
        alert('Algebraic expression(s) in the variable expression(s) @{..}@ invalid');
        return [];
    }
    var symbols = [];
    var char;
    var run = false;
    var sub_index;
    for (let index = 0; index < expression.length; index++) {
      char = expression.charAt(index);
      
        if (/[a-zA-Z]/.test(char) && expression.charAt(index-1) != '_') {
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
    symbols = symbols.filter(item => !/^e[+-]?\d+$/.test(item));
    // console.log(`Symbols from extract symbols: ${symbols}`)
    return symbols
  }






  //-----------------------------HANDLING VARIABLES---------------------------------------//

  
  const addVarBtn = document.querySelector('.var-btn');
  const varInfoDiv = document.querySelector('.var-info-div');
  const createdVarsDiv = document.querySelector('.created-vars');

  var symbol = '';
  var enteredDomain = '';
  varInfoDiv.style.opacity = '0';
  varInfoDiv.style.height = '0';
  varInfoDiv.style.width = '0';
  var state = 'closed';
  addVarBtn.addEventListener('click', (event) => {
    event.preventDefault();
    if (state === 'closed') {
      state = 'open';
      addVarBtn.innerHTML = '-';
      varInfoDiv.style.width = 'auto';
      varInfoDiv.style.height = 'auto'; // Set height to 'auto' to reveal content
      varInfoDiv.style.opacity = '1';   // Set opacity to '1' to reveal content
      varInfoDiv.style.overflow = 'visible'; // Set overflow to 'visible' to reveal content
    } else if (state === 'open') {
      state = 'closed';
      addVarBtn.innerHTML = '+';
      varInfoDiv.style.width = '0';
      varInfoDiv.style.height = '0';    // Set height to '0' to hide content
      varInfoDiv.style.opacity = '0';   // Set opacity to '0' to hide content
      varInfoDiv.style.overflow = 'hidden'; // Set overflow to 'hidden' to hide content
    }
  });
  
  
  varInfoDiv.addEventListener('click', (event)=>{
      //event.preventDefault();
      if(event.target.classList.contains('btn-create-var')){
          const varSymbolField = varInfoDiv.querySelector('.var-symbol');
          const varDomainField = varInfoDiv.querySelector('.var-domain');
          const varStepSize = varInfoDiv.querySelector('.var-step-size');
          const intRadio = varInfoDiv.querySelector('input[name="varType"][value="int"]');
          const floatRadio = varInfoDiv.querySelector('input[name="varType"][value="float"]');
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
          else if ((symbol.length === 2) || (/^[a-zA-Z]$/.test(symbol.charAt(0)) === false) || 
          ((symbol.charAt(1) != '_') && (symbol.length>=3))){
              alert('Invalid symbol');
              return;
          }else if(symbol.length > 10){
            alert('Symbol cannot be more than 10 characters');
            return;
          }
          // Checking whether domain entered is valid
          enteredDomain = varDomainField.value;
          var parsedDomain = parseDomainInput(enteredDomain);
          if(parsedDomain.length === 0){
              alert('Invalid domain');
              return;
          }

          // Checking if the step size is valid
          if(varStepSize.value.length >= 1 && isNaN(parseFloat(varStepSize.value))){
                alert('Step size must be an int or float');
                return
          } else if(varStepSize.value.length == 0){
            varStepSize.value = 0 // if no step size is given.
          }
        
          // passed all the tests
          varSymbolsArray.push(symbol); // adding the symbol to the list of symbols.
          const newVarDiv = document.createElement('div');
          const newVarBtn = document.createElement('button');
          newVarBtn.type = 'button';
          newVarBtn.classList.add('btn', 'btn-warning'); // Separate the classes
          if(symbol.length >=3){
            newVarBtn.innerHTML = `${symbol.charAt(0)}<sub>${symbol.slice(2)}</sub>`
          }else{
            newVarBtn.innerHTML = symbol; // if symbol is one character.
          }
          
          newVarDiv.appendChild(newVarBtn);
          newVarDiv.classList.add('variable');
          newVarDiv.setAttribute('data-symbol', symbol);
          
          // Putting the variable type and step size in hidden input fields.
            
            // Var Type
          const varTypeHiddenInput = document.createElement('input');
          varTypeHiddenInput.type = 'hidden';
          varTypeHiddenInput.name = `var#type#${symbol}`
          if(intRadio.checked){
            varTypeHiddenInput.value = '0'
          } else {
            varTypeHiddenInput.value = '1'
          }
          
          // Step size
          const stepSizeHiddenInput = document.createElement('input');
          stepSizeHiddenInput.type = 'hidden';
          stepSizeHiddenInput.name = `step#size#${symbol}`
          stepSizeHiddenInput.value = varStepSize.value

          // appending the hidden inputs to varBtn
          newVarBtn.appendChild(varTypeHiddenInput);
          newVarBtn.appendChild(stepSizeHiddenInput);

          for (let i = 0; i < parsedDomain.length; i++) {
              // Getting the variable intervals.
              const domainLbHiddenInput = document.createElement('input');
              domainLbHiddenInput.type = 'hidden';
              domainLbHiddenInput.name = `domain#lb#${symbol}#${i}`//domain lower bound
              domainLbHiddenInput.value = parsedDomain[i].lower
              
              const domainUbHiddenInput = document.createElement('input');
              domainUbHiddenInput.type = 'hidden';
              domainUbHiddenInput.name = `domain#ub#${symbol}#${i}`//domain upper bound
              domainUbHiddenInput.value = parsedDomain[i].upper

              newVarBtn.appendChild(domainLbHiddenInput);
              newVarBtn.appendChild(domainUbHiddenInput);
          }
          
          createdVarsDiv.appendChild(newVarDiv);
          createdVarsDiv.scrollIntoView({behavior:"smooth"});
          varInfoDiv.style.opacity = '0';
          varInfoDiv.style.height = '0';
          varInfoDiv.style.width = '0';
          state ='closed';
          addVarBtn.innerHTML = '+';

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
                    if (lowerBound >= upperBound) {
                        alert("Lower bound must be less than upper bound!");
                        boundsArray.length = 0; // Clear the array
                        return boundsArray; // Exit the function
                    }else if (lowerBound < -1000 || upperBound > 1000){
                        alert('Magnitude of bound must be less than 1000');
                        boundsArray.length = 0;
                        return boundsArray;
                    } else {
                        boundsArray.push({ lower: lowerBound, upper: upperBound });
                    }
                }
            }
        });
    }

    return boundsArray;
}
  







// ---------------------------------PREFACE AND UNITS ---------------------------//

const prefaceUnitsBtns = document.querySelectorAll('.plus-sign')

prefaceUnitsBtns.forEach((btn)=>{
    btn.addEventListener('click', ()=>{
        if(!btn.classList.contains('open')){ // closed state
            btn.parentNode.querySelector('input').style.display = 'block';
            btn.textContent = '-'
            btn.classList.add('open');
        }else { // open state
            btn.parentNode.querySelector('input').style.display = 'none';
            btn.textContent = '+'
            btn.classList.remove('open');
        }

    })
})







settingsSelect.addEventListener('change', (event)=>{
    var inputsWithSettingsClass = document.querySelectorAll('input.settings');
    inputsWithSettingsClass.forEach((sInput)=>{
        // Updating the previous hidden inputs
        const settingsHiddenInput = document.querySelector(`input[name="${parseInt(settingsPreviousValue)}_${sInput.name}"]`);
        if(settingsHiddenInput){// in case it has been deleted
            settingsHiddenInput.value = sInput.value; 
        }


        // updating the displayed settings to the current option

        sInput.value = document.querySelector(`input[name="${parseInt(event.target.value)}_${sInput.name}"]`).value
   
   })
   settingsPreviousValue = event.target.value
})

// ---------------------------------MAKING THE QUESTION MULTIPART------------------------------------------//

function addQuestionBlock(){

    // creating new option in settings
    const newSettingsOption = document.createElement('option');
    newSettingsOption.classList.add(`settings-option-${num_questions}`);
    newSettingsOption.value = `${num_questions}`
    newSettingsOption.innerHTML = `Part ${String.fromCharCode(64 + part_num_questions)}`;
    const pts = initial_num_points/(part_num_questions) | 0;// to convert to integer
    settingsSelect.appendChild(newSettingsOption);
    // each time a new part is added, the number of points is redistributed.
    // this is not very nice because if the instructor changed them earlier
    // it will be changed again but I don't think that's too much of a big deal.
    document.querySelector('.init-num-pts').value = pts;
    const hiddenNumberPts = document.querySelectorAll('.h-num-pts');// this does not include the h-num-pts in the new block
    // We take care of that in the questionBluePrint below
    hiddenNumberPts.forEach((hnp)=>{
        hnp.value = pts
    })

    const questionBluePrint = `
    <input type="hidden" value=${num_questions} class="question-number-value">
    <div class="question-content form-group">
         <label class="q-label-title">Question ${String.fromCharCode(64 + part_num_questions)}:</label><br/>
         <textarea placeholder="Enter the content of the question" class="question-textarea w-100 question-input-field" name="${num_questions}_question_text"></textarea>
     </div>
     <div class="main-question-image-preview" data-counter="0"></div>
     <div class="uploaded-question-preview"></div>
     <button type="button" class="main-question-add-image-btn btn btn-light open">Upload Image</button>
     <div class="question-image-upload-section" style="display: none;">
       <input type="text" placeholder="Enter image label" class="image-label-input-field field-style"/>
       <input type="file" accept="image/*" class="main-question-image-input">
       <button type="button" class="btn btn-success question-image-add">add</button>
     </div>
     <br/>
    
     <div class="answer-options">
       
       <label>Select answer type</label><br/>
       <input type="hidden" value="none" class="hidden-q-type"/>
       <input type="hidden" placeholder="0" name="${num_questions}_answer" class="q-answer-hidden"/>
       <input type="hidden" placeholder="units" name="${num_questions}_answer_unit" class="q-answer-units-hidden"/>
       <input type="hidden" placeholder="latex preface" name="${num_questions}_answer_preface" class="q-answer-preface-hidden"/>
       <button type="button" id="expression-btn" class="expression-btn btn btn-primary exempt">Expression</button>
       <button type="button" id="float-btn" class="float-btn btn btn-info exempt">Float</button>
       <button type="button" id="mcq-btn" class="mcq-btn btn btn-light exempt">MCQ</button>
       <button type="button" id="mp-btn" class="mp-btn btn btn-dark exempt">Matching Pairs</button>
       <button type="button" id="fr-btn" class="fr-btn btn btn-secondary exempt" style="display:none;">Free Response</button>
       <button type="button" id="survey-btn" class="survey-btn btn btn-dark exempt" style="display: none;">Survey</button>
       <button type="button" id="latex-btn" class="latex-btn btn btn-secondary exempt"  style="display: none;">Latex</button>
       
     </div>
    
     <div class="mcq-answers">
       <div class="mcq-options-button" style="display: none;">
         <label>Select MCQ type</label><br/>
         <button type="button" data-qid="mcq-expression-btn" class="mcq-expression-btn btn-primary exempt">Expression mode</button>
         <button type="button" data-qid="mcq-float-btn" class="mcq-float-btn btn-info exempt">Float mode</button>
         <button type="button" data-qid="mcq-text-btn" class="mcq-text-btn btn-light exempt">Text mode</button>
         <button type="button" data-qid="mcq-latex-btn" class="mcq-latex-btn btn-secondary exempt">Latex mode</button>
         <button type="button" data-qid="mcq-image-btn" class="mcq-image-btn btn-dark exempt">Image mode</button>
       </div>
       <div class="inputed-mcq-answers" data-counter="0" data-true-counter="0">
    
       </div>
       <br/>
       <div class="mcq-image-preview"></div>
       <br/>
       <div class="mcq-input-div" style="display: none;">
         <input style="width: 100%; box-sizing: border-box;" type="text" class="mcq-input-field field-style"/>
         <input type="file" accept="image/*" class="image-upload-input-field" style="display:none;"/>
         <button type="button" class="btn btn-success mcq-add">add</button>
       </div>
    
     </div>

     <div class="mp-answers">
        <div class="inputed-mp-answers" data-counter="0" data-qnumber="${num_questions}" data-mere-counter="0">
        </div>
        <br/>
        <div class="mp-input-div" style="display:none;">
            <div class="mp-inputs">
                <input type="text" class="field-style mp-input-field-a" placeholder="Enter part A"/>
                <input type="text" class="field-style mp-input-field-b" placeholder="Enter matching part B"/>
            </div>
            <div>
                <button type="button" class="btn btn-success mp-add">add</button>
            </div>
        </div>
     </div>
     
     <div class="answer-fields">
         
     </div>
     <div class="formatted-answer structural-formatted-answer"></div>
     <br/>
     <div class="calculator-area-div"></div><br/>
     <div class="hints-section"  data-counter="0">
        <div class="inputed-hints">
        </div>
        <div class="add-hint-section" style="display:none;"/>
            <input type="text" placeholder="Enter hint and click add" class="field-style add-hint-input-field"/>
            <br/>
            <button type="button" class="add-inputed-hint-btn btn btn-success"> add </button>
        </div>
        <button type="button" class="add-hint-btn btn btn-outline-info open"> Add Hint </button>
     </div>
     <hr/>
     <button class="btn btn-outline-success check-question-btn">Add Part ${String.fromCharCode(64 + part_num_questions + 1)}</button>
     <br/><br/>
     <div class="hidden-settings">
            <input class="field-style hidden-settings h-num-pts" type="hidden" name="${num_questions}_num_points" value="${pts}"/>
            <input class="field-style hidden-settings" type="hidden" name="${num_questions}_max_num_attempts"/>
            <input class="field-style hidden-settings" type="hidden" name="${num_questions}_deduct_per_attempt"/>
            <input class="field-style hidden-settings" type="hidden" name="${num_questions}_margin_error"/>
            <input class="field-style hidden-settings" type="hidden" name="${num_questions}_percentage_pts_units"/>
            <input class="field-style hidden-settings" type="hidden" name="${num_questions}_max_mcq_num_attempts">
            <input class="field-style hidden-settings" type="hidden" name="${num_questions}_mcq_deduct_per_attempt"/>
            <input class="field-style hidden-settings" type="hidden" name="${num_questions}_units_num_attempts"/>
     </div>
    `



    const questionBlock = document.createElement('div');
    questionBlock.classList.add('question-block');
    questionBlock.innerHTML = questionBluePrint;
    const answerOptionsDiv = questionBlock.querySelector('.answer-options');
    const expressionBtn = questionBlock.querySelector('.expression-btn');
    const answerFieldsDiv = questionBlock.querySelector('.answer-fields');
    const mcqAnswersDiv = questionBlock.querySelector('.mcq-answers');
    const mcqBtn = questionBlock.querySelector('.mcq-btn');
    const mpBtn = questionBlock.querySelector('.mp-btn');
    const mcqOptionBtnsDiv = mcqAnswersDiv.querySelector('.mcq-options-button');
    const inputedMcqAnswersDiv = questionBlock.querySelector('.inputed-mcq-answers');
    const inputedMpAnswersDiv = questionBlock.querySelector('.inputed-mp-answers');
    const imgLabelInputField = questionBlock.querySelector('.image-label-input-field');
    const questionAddImgBtn = questionBlock.querySelector('.main-question-add-image-btn');
    const questionImgUploadSection = questionBlock.querySelector('.question-image-upload-section');
    const uploadedQuestionPreview = questionBlock.querySelector('.uploaded-question-preview');
    const hintSectionDiv = questionBlock.querySelector('.hints-section');



    const addQuestionImgBtn = questionBlock.querySelector('.question-image-add');
    const addMcqOptionBtn = questionBlock.querySelector('.mcq-add');
    const addMpOptionBtn = questionBlock.querySelector('.mp-add');
    const mcqInputDiv = questionBlock.querySelector('.mcq-input-div');
    const mcqInputField = mcqInputDiv.querySelector('.mcq-input-field');
    const mpInputDiv = questionBlock.querySelector('.mp-input-div');
    const mpInputFieldA = mpInputDiv.querySelector('.mp-input-field-a');
    const mpInputFieldB = mpInputDiv.querySelector('.mp-input-field-b');
    const mcqImagePreview = questionBlock.querySelector('.mcq-image-preview');
    const imageUploadInput = questionBlock.querySelector('.image-upload-input-field');
    const floatBtn = questionBlock.querySelector('.float-btn');
    const latexBtn = questionBlock.querySelector('.latex-btn');
    const frBtn = questionBlock.querySelector('.fr-btn');
    const surveyBtn = questionBlock.querySelector('.survey-btn');
    latexBtn.style.display = 'none';
    const formattedAnswerDiv = questionBlock.querySelector('.structural-formatted-answer');

    const mainQuestionImageInput = questionBlock.querySelector('.main-question-image-input');
    const mainQuestionImagePreview = questionBlock.querySelector('.main-question-image-preview');
    const checkButton = questionBlock.querySelector('.check-question-btn');
    const hiddenQuestionType = questionBlock.querySelector('.hidden-q-type');
    const calculatorAreaDiv = questionBlock.querySelector('.calculator-area-div');


    // setting the initial hidden settings

var inputsWithSettingsClass = document.querySelectorAll('input.settings');
inputsWithSettingsClass.forEach((input)=>{
     const question_num = parseInt(questionBlock.querySelector('.question-number-value').value)
     const settingsHiddenInput = questionBlock.querySelector(`input[name="${question_num}_${input.name}"]`);
     settingsHiddenInput.value = input.value;

})

    answerOptionsDiv.addEventListener('click', () => {
        const displayDiv = screen.closest('.calc-display-div');
        const previousQuestionBlock = screen.closest('.question-block');
        const mappings = [
            { source: '.q-answer-preface-hidden', target: '.preface-screen' },
            { source: '.q-answer-hidden', target: '#screen' },
            { source: '.q-answer-units-hidden', target: '.units-screen' }
        ];
        // if previousQuestionBlock and current block are different
        if(previousQuestionBlock){
            if(previousQuestionBlock != questionBlock){
                mappings.forEach((mapping)=>{
                    // update the previous block hidden inputs
                    const calcField = displayDiv.querySelector(mapping.target);
                    previousQuestionBlock.querySelector(mapping.source).value = calcField.value;
                    // Now change the calculator fields
                    const newfield = questionBlock.querySelector(mapping.source) 
                    calcField.value = newfield.value
                    calcField.placeholder = newfield.placeholder;
                    if(calcField.value.length > 1){
                        calcField.style.display = 'block';
                        prefaceUnitsBtns.forEach((btn)=>{
                                if(!btn.classList.contains('open')){ // closed state
                                    btn.parentNode.querySelector('input').style.display = 'block';
                                    btn.textContent = '-'
                                    btn.classList.add('open');
                                }else { // open state
                                    btn.parentNode.querySelector('input').style.display = 'none';
                                    btn.textContent = '+'
                                    btn.classList.remove('open');
                                }
                        
                           
                        })
                        
                    }else if(mapping.target != "#screen"){
                        calcField.style.display = 'none';
                        prefaceUnitsBtns.forEach((btn)=>{
                            if(!btn.classList.contains('open')){ // closed state
                                btn.parentNode.querySelector('input').style.display = 'block';
                                btn.textContent = '-'
                                btn.classList.add('open');
                            }else { // open state
                                btn.parentNode.querySelector('input').style.display = 'none';
                                btn.textContent = '+'
                                btn.classList.remove('open');
                            }
                    
                       
                    })
                    }


                })
            } else {
                // in case the previous block is the same as the current block, 
                // update the hidden fields of the current block.
                mappings.forEach((mapping)=>{
                // update the previous block hidden inputs
                const calcField = displayDiv.querySelector(mapping.target);
                previousQuestionBlock.querySelector(mapping.source).value = calcField.value;
                if(calcField.value.length > 1){
                    calcField.style.display = 'block';
                }else if(mapping.target != "#screen"){
                    calcField.style.display = 'none';
                }

                })
            }
        }

    
        calculatorAreaDiv.innerHTML = '';
        calculatorAreaDiv.appendChild(displayDiv.closest('#calc-container'));
    });
    


///

/// ATTENTION! WARNING! IMPORTANT! Recursion here.
checkButton.addEventListener('click', (event)=>{
    event.preventDefault();

    const displayDiv = screen.closest('.calc-display-div');
    const previousQuestionBlock = screen.closest('.question-block');
    const mappings = [
        { source: '.q-answer-preface-hidden', target: '.preface-screen' },
        { source: '.q-answer-hidden', target: '#screen' },
        { source: '.q-answer-units-hidden', target: '.units-screen' }
    ];
    if(previousQuestionBlock == questionBlock){ // if the screen is in the current question block.
        mappings.forEach(mapping=>{
            questionBlock.querySelector(mapping.source).value = displayDiv.querySelector(mapping.target).value;
        })
    }


    if(checkButton.classList.contains('btn-outline-success')){
        if(checkQuestionBlock(questionBlock)){
            const newQuestionBlock = addQuestionBlock()
            allQuestionBlocks.appendChild(newQuestionBlock);
            checkButton.classList.remove('btn-outline-success');
            checkButton.classList.add('btn-outline-danger');
            checkButton.innerHTML = 'Delete Part ' + String.fromCharCode(checkButton.innerHTML.charCodeAt(checkButton.innerHTML.length - 1) - 1);
            newQuestionBlock.scrollIntoView({behavior: "smooth"});
        }
    }else{// Delete block;
        const val = questionBlock.querySelector('.question-number-value').value;
        delete questionTypeDicts[val];
        questionBlock.parentNode.removeChild(questionBlock);
        //num_questions -= 1;
        const correspondingSettingsOption = settingsSelect.querySelector(`.settings-option-${val}`);
        if (correspondingSettingsOption) {
            settingsSelect.removeChild(correspondingSettingsOption);
        }
        part_num_questions -= 1;
        // Renaming the question titles.
        const allqBlocks = document.querySelectorAll('.question-block');
        let count = 1;
        let optionCounter = 1;
        const allSettingsOptions = settingsSelect.querySelectorAll('option');
        allSettingsOptions.forEach((sO)=>{
            sO.innerHTML = `Part ${String.fromCharCode(64 + optionCounter)}`;
            optionCounter += 1;
        })

        allqBlocks.forEach((qBlock) => {
            const labelTitle = qBlock.querySelector('.q-label-title');
            const checkBtn = qBlock.querySelector('.check-question-btn');
            // 'Question B:' -> 'Question A:'
            labelTitle.textContent = labelTitle.textContent.slice(0, -2) + String.fromCharCode(64 + count) + labelTitle.textContent.slice(-1);
            if(checkBtn.classList.contains('btn-outline-success')){
             checkBtn.textContent = checkBtn.textContent.slice(0, -1) + String.fromCharCode(64 + count + 1);
            }else{
            checkBtn.textContent = checkBtn.textContent.slice(0, -1) + String.fromCharCode(64 + count);
            }
            count = count + 1;
        });
    }

    // TODO: Implement what happens when all the checks have passed.
})


/*-----------------------------------------SURVEY QUESTION-----------------------------------*/
surveyBtn.addEventListener('click', (event)=> {
    event.preventDefault();
    hiddenQuestionType.value = 's-answer';
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

mcqBtn.addEventListener('click', (event)=>{
// If the instructor chooses mcq as the answer option.
event.preventDefault();
    inputedMcqAnswersDiv.style.display = 'block';
    inputedMpAnswersDiv.style.display = 'none';
    mcqImagePreview.style.display = 'block';
    hiddenQuestionType.value = 'm-answer'
    formattedAnswerDiv.style.display = 'none';
    calculatorDiv.style.display = 'none';
    mcqOptionBtnsDiv.style.display = 'block';
    questionTypeDicts[questionBlock.querySelector('.question-number-value').value] = '3'; 

});
mpBtn.addEventListener('click', (event)=>{
    // If the instructor chooses mcq as the answer option.
    event.preventDefault();
        inputedMcqAnswersDiv.style.display = 'none';
        inputedMpAnswersDiv.style.display = 'block';
        mcqImagePreview.style.display = 'none';
        hiddenQuestionType.value = 'mp-answer'
        formattedAnswerDiv.style.display = 'none';
        calculatorDiv.style.display = 'none';
        mcqOptionBtnsDiv.style.display = 'none';
        mpInputDiv.style.display = 'block';
        questionTypeDicts[questionBlock.querySelector('.question-number-value').value] = '8'; 
    
    });

mcqOptionBtnsDiv.addEventListener('click', (event) => {
    event.preventDefault();

    mcqInputDiv.style.display = 'block';
    imageUploadInput.style.display = 'none';
    mcqImagePreview.style.display = 'none';
    mcqInputField.value = '';

    const config = {
        'mcq-expression-btn': {
            placeholder: 'Enter expression and click add',
            answerType: 'e-answer'
        },
        'mcq-float-btn': {
            placeholder: 'Enter float and click add',
            answerType: 'f-answer'
        },
        'mcq-text-btn': {
            placeholder: 'Enter text and click add',
            answerType: 't-answer'
        },
        'mcq-latex-btn': {
            placeholder: 'Enter latex and click add',
            answerType: 'l-answer'
        },
        'mcq-image-btn': {
            placeholder: 'Enter image label and click add',
            answerType: 'i-answer',
            displayImageUpload: true
        }
    };

    const btnConfig = config[event.target.dataset.qid];
    
    if (btnConfig) {
        mcqInputField.placeholder = btnConfig.placeholder;
        mcqInputField.setAttribute('data-answer-type', btnConfig.answerType);

        if (btnConfig.displayImageUpload) {
            imageUploadInput.style.display = 'block';
            mcqImagePreview.style.display = 'block';
        }
    }
});


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
            const holder = parseInt(inputedMcqAnswersDiv.dataset.counter)
            inputedMcqAnswersDiv.dataset.counter = `${holder + 1}`;
        }
        catch(error){
            console.log(error)
            alert('Make sure you enter the correct format of the answer type you selected.')
        }
        
    }


})

addMpOptionBtn.addEventListener('click', (event)=>{
    event.preventDefault();
    // Adding an mcq option after filling the input field.
    // This may look small but it's the most dense function in this file
    // Checkout create_inputed_mcq_div() to see what I mean.
    if ((mpInputFieldA.value === null || mpInputFieldA.value ==='') || (mpInputFieldB.value === null || mpInputFieldB.value ==='')){
        alert('Cannot create an empty matching pair option.')
        
    }
    else{
        try{
            const qnumber = inputedMpAnswersDiv.dataset.qnumber
            const holder = parseInt(inputedMpAnswersDiv.dataset.counter)
            const holder2 = parseInt(inputedMpAnswersDiv.dataset.mereCounter)
            // Creating the box of inputed matching pairs for the user.
            const formatted_mp = document.createElement('div');
            formatted_mp.innerHTML = `
                <div class="formatted-answer">
                <input type="hidden" value="${mpInputFieldA.value}" name="${qnumber + '_' + holder + '_mp_a'}"/>
                ${mpInputFieldA.value}
                </div>
                <div class="formatted-answer">
                <input type="hidden" value="${mpInputFieldB.value}" name="${qnumber + '_' + holder + '_mp_b'}"/>
                ${mpInputFieldB.value}
                </div>
            `
            const delDiv = document.createElement('div');
            delDiv.innerHTML = '<button  type="button" class="btn btn-danger mp-delete exempt">delete</button><br/>'
            delDiv.classList.add('add-delete-btns')
            formatted_mp.classList.add('formatted-mp', 'inputed-mp-answer');
            
            // Creating and populating hidden input fields. 

            inputedMpAnswersDiv.appendChild(formatted_mp);
            formatted_mp.appendChild(delDiv);
            mpInputFieldA.value = '';
            mpInputFieldB.value = '';
            inputedMpAnswersDiv.dataset.counter = `${holder + 1}`;
            inputedMpAnswersDiv.dataset.mereCounter = `${holder2 + 1}`;
        }
        catch(error){
            console.log(error)
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
        const holder =  parseInt(inputedMcqAnswersDiv.dataset.trueCounter)
        inputedMcqAnswersDiv.dataset.trueCounter = `${holder + 1}`;
        const answer_info_input = target.closest('.inputed-mcq-answer').querySelector('.answer_info');
        answer_info_input.value = rep(answer_info_input.value, 0, '1');
    } else if(target.classList.contains('mcq-true')){
        // changing an mcq option from true to false.
        target.classList.add('mcq-false','btn-warning');
        target.classList.remove('mcq-true', 'btn-info');
        target.innerHTML = 'False'; 
        const holder = parseInt(inputedMcqAnswersDiv.dataset.trueCounter);
        inputedMcqAnswersDiv.dataset.trueCounter = `${holder - 1}`;    
        const answer_info_input = target.closest('.inputed-mcq-answer').querySelector('.answer_info');
        answer_info_input.value = rep(answer_info_input.value, 0, '0');
    } else if (target.classList.contains('mcq-delete')){
        // deleting an mcq option.
        const holder = parseInt(inputedMcqAnswersDiv.dataset.counter)
        inputedMcqAnswersDiv.dataset.counter  = `${holder-1}`;
        if (target.classList.contains('mcq-true')){
            const holder = parseInt(inputedMcqAnswersDiv.dataset.trueCounter)
            inputedMcqAnswersDiv.dataset.trueCounter = `${holder-1}`;
        }
        inputedMcqAnswersDiv.removeChild(target.closest('.inputed-mcq-answer'));//TODO: Can probably make this something better.
    }
})

inputedMpAnswersDiv.addEventListener('click', (event)=>{
    event.preventDefault();
    if(event.target.classList.contains('mp-delete')){
        const holder = parseInt(inputedMpAnswersDiv.dataset.mereCounter);
        inputedMpAnswersDiv.dataset.mereCounter = `${holder -1}`;
        inputedMpAnswersDiv.removeChild(event.target.closest('.inputed-mp-answer'));
    }
})

///EVENT LISTENERS ////////////////////////////////////////////////////////////////////////////////




/*------------------------------------------STRUCTURAL QUESTION --------------------------------- */
// latexAnswerDiv is never used but just keeping it here.
const latexAnswerDiv = `
<div class="l-answer"><br/>
<label>Latex Answer:</label>
    <input style="width: 100%; box-sizing: border-box;" class="question-input-field" placeholder="Enter LaTex" type="text" class="latex-answer-input" name="${num_questions}_answer"/>
    </div>
`
// Free response button selected.
frBtn.addEventListener('click', (event)=>{
    event.preventDefault();
    hiddenQuestionType.value = 'fr-answer';  
    inputedMcqAnswersDiv.style.display = 'none';
    inputedMpAnswersDiv.style.display = 'none';
    formattedAnswerDiv.innerHTML = 'Free response mode selected.'
    formattedAnswerDiv.style.display = 'block';
    mcqOptionBtnsDiv.style.display = 'none';
    mcqInputDiv.style.display = 'none';
    mpInputDiv.style.display = 'none';
    mcqImagePreview.style.display = 'none';
    calculatorDiv.style.display = 'none';
    answerFieldsDiv.innerHTML = '';
    
    formattedAnswerDiv.scrollIntoView({behavior: 'smooth'});
    questionTypeDicts[questionBlock.querySelector('.question-number-value').value] = '4';
     
})

// Expression answer button selected.
expressionBtn.addEventListener('click', (event)=> {
    event.preventDefault();
    hiddenQuestionType.value = 'e-answer';
    inputedMcqAnswersDiv.style.display = 'none';
    inputedMpAnswersDiv.style.display = 'none';
    formattedAnswerDiv.style.display = 'block';
    mcqOptionBtnsDiv.style.display = 'none';
    mcqInputDiv.style.display = 'none';
    mpInputDiv.style.display = 'none';
    mcqImagePreview.style.display = 'none';
    calculatorDiv.style.display = 'flex';
    answerFieldsDiv.innerHTML = '';
    screen.placeholder = 'Expression';

    answerFieldsDiv.scrollIntoView({ behavior: 'smooth' });
    questionTypeDicts[questionBlock.querySelector('.question-number-value').value] = '0';

});

// Float button selected.
floatBtn.addEventListener('click', function(event) { 
    event.preventDefault();
    hiddenQuestionType.value = 'f-answer';
    inputedMcqAnswersDiv.style.display = 'none';
    inputedMpAnswersDiv.style.display = 'none';
    formattedAnswerDiv.style.display = 'block';
    mcqOptionBtnsDiv.style.display = 'none';
    mcqInputDiv.style.display = 'none';
    mpInputDiv.style.display ='none';
    mcqImagePreview.style.display = 'none';
    calculatorDiv.style.display = 'flex';
    answerFieldsDiv.innerHTML = '';
    screen.placeholder = 'Real number';

    answerFieldsDiv.scrollIntoView({ behavior: 'smooth' });
    questionTypeDicts[questionBlock.querySelector('.question-number-value').value] = '1';
});

// Latex button selected. Probably never used.
latexBtn.addEventListener('click', (event)=> {
    event.preventDefault();
    hiddenQuestionType.value = 'l-answer'
    inputedMpAnswersDiv.style.display = 'none';
    formattedAnswerDiv.style.display = 'block';
    mcqOptionBtnsDiv.style.display = 'none';
    mcqInputDiv.style.display = 'none';
    mpInputDiv.style.display = 'none';
    mcqImagePreview.style.display = 'none';
    calculatorDiv.style.display = 'none';
    answerFieldsDiv.innerHTML = latexAnswerDiv;
    answerFieldsDiv.scrollIntoView({ behavior: 'smooth' });

    questionTypeDicts[questionBlock.querySelector('.question-number-value').value] = '2'



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


//-------------------------HINTS--------------------------------------------

hintSectionDiv.addEventListener('click', (event)=>{
    event.preventDefault();
    const inputedHints = hintSectionDiv.querySelector('.inputed-hints')
    if(event.target.classList.contains('add-hint-btn')){
        const addHintSection = hintSectionDiv.querySelector('.add-hint-section');
        addHintSection.style.display = 'block';
        event.target.style.display = 'none';

    }else if(event.target.classList.contains('delete-hint-btn')){
        inputedHints.removeChild(event.target.closest('.hint-div'));
        //const holder = hintSectionDiv.dataset.counter
        //hintSectionDiv.dataset.counter = `${parseInt(holder) - 1}`;
    }else if(event.target.classList.contains('add-inputed-hint-btn')){
        const hintInputField = event.target.closest('.add-hint-section').querySelector('.add-hint-input-field');
        if(hintInputField.value.length < 1){
            alert('Cannot add empty hint');
            return
        }else{
            const newHintDiv = create_hint_div(hintInputField);
            inputedHints.appendChild(newHintDiv);
            const holder = hintSectionDiv.dataset.counter
            hintSectionDiv.dataset.counter = `${parseInt(holder) + 1}`;

        }
    }
})



//------------------------------------IMAGE UPLOAD HANDLING FOR MAIN QUESTION-------------------
// Expanding image upload section
questionAddImgBtn.addEventListener('click', (event)=>{
    event.preventDefault();
    if(questionAddImgBtn.classList.contains('open')){
        questionAddImgBtn.classList.remove('open');
        questionAddImgBtn.classList.add('closed');
        questionAddImgBtn.innerHTML = '-collapse-';
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



addQuestionImgBtn.addEventListener('click', (event)=>{
    event.preventDefault();
    if (imgLabelInputField.value === null || imgLabelInputField.value ==='') {
        alert('You must enter a label for the image.');
        return;
    }
    if(mainQuestionImageInput.files.length === 0){
        alert('You must choose an image file.');
        return
    }

    try{
        const formatted_new_img = create_img_div(mainQuestionImageInput, imgLabelInputField.value);
        mainQuestionImagePreview.appendChild(formatted_new_img);
        imgLabelInputField.value = '';
        const holder = parseInt(mainQuestionImagePreview.dataset.counter)
        mainQuestionImagePreview.dataset.counter =  `${holder + 1}`;
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
        mainQuestionImagePreview.removeChild(target.closest('.question-image'));
    }
})



function create_img_div(img_input_field, img_label){
    const qnum = questionBlock.querySelector('.question-number-value').value;
    var imgDiv = document.createElement('div');
    var imgLabel = document.createElement('p');
    imgLabel.innerHTML = img_label;
    imgDiv.className = 'question-image';
    imgDiv.innerHTML = `
    <br/>
    <div class="formatted-answer-option"></div>
    <input value="${img_label}" type="hidden" name="${qnum}_question_image_label_${mainQuestionImagePreview.dataset.counter}"/>
    <div class="add-delete-btns">
        <button  type="button" class="btn btn-danger img-delete exempt">delete</button>
    </div>
`;
    var formattedImgDiv = imgDiv.querySelector('.formatted-answer-option');
    formattedImgDiv.appendChild(imgLabel);
    formattedImgDiv.appendChild(uploadedQuestionPreview.cloneNode(true));
    const image_input_field_clone = img_input_field.cloneNode(true);
    image_input_field_clone.name = `${qnum}_question_image_file_${mainQuestionImagePreview.dataset.counter}`;
    image_input_field_clone.style.display = 'none';
    formattedImgDiv.appendChild(image_input_field_clone);
    uploadedQuestionPreview.innerHTML = '';
    img_input_field.value = '';

    return imgDiv;
}


function create_hint_div(hint_input_field){
    const qnum = questionBlock.querySelector('.question-number-value').value;
    var hintDiv = document.createElement('div');
    const hintSection = hint_input_field.closest('.hints-section');
    hintDiv.className = 'hint-div';
    hintDiv.innerHTML = `
    <br/>
    <div class="formatted-answer-option">${hint_input_field.value}</div>
    <input type="hidden" value="${hint_input_field.value}" name="${qnum}_hint_${hintSection.dataset.counter}"/>
    <div class="add-delete-btns">
        <button type="button" class="delete-hint-btn btn btn-danger">delete</button>
    </div>
    <br/>
    `
    hint_input_field.value = '';
    return hintDiv;
}




function create_inputed_mcq_div(input_field, answer_type) {
    const qnum = questionBlock.querySelector('.question-number-value').value;
    var answer_value = input_field.value
    var inputedMcqDiv = document.createElement('div'); // to be appended to .inputed-mcq-answers.
    inputedMcqDiv.className = 'inputed-mcq-answer';
    var processedString, simplifiedString;
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
                processedString = processString(answer_value)
                simplifiedString = math.simplify(processedString)
                answer_value = simplifiedString.evaluate();
                if(typeof(answer_value) != 'number'){
                    alert('You selected float mode but the answer you provided is not a float');
                    return;
                }
                
            }catch {
                if(validateText(answer_value, varSymbolsArray, isFloat=true)){
                    display_value = answer_value;
                }else{

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
                processedString = processString(answer_value)
                simplifiedString = math.simplify(processedString)
                answer_value = simplifiedString.toString();
                display_value = answer_value;
            }
            catch{
                const holder = parseInt(inputedMcqAnswersDiv.dataset.counter)
                inputedMcqAnswersDiv.dataset.counter  = `${holder - 1}`;
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
            else if(answer_type==='i-answer'){
                formatted_answer = document.createElement('p');
                formatted_answer.innerHTML = display_value;  
            }
            else {
                try{
                    //const userInputNode = math.simplify(processedString);
                    userInputLatex = math.parse(processedString).toTex();
                    formatted_answer = MathJax.tex2chtml(userInputLatex + '\\phantom{}');
                }catch{
                    formatted_answer = document.createElement('p');
                    formatted_answer.innerHTML = display_value;
                }
                
            }
            

            // Now that the formatted_answer is ready, create the necessary HTML structure
            var mcqAnswerDiv = document.createElement('div');
            if (answer_type != 'i-answer'){
                mcqAnswerDiv.innerHTML = `
                <br/>
                <div class="formatted-answer-option unexpand"></div>
                <input value="${answer_value}" type="hidden" name="${qnum}_answer_value_${inputedMcqAnswersDiv.dataset.counter}"/>
                <input value="${answer_info_encoding}" type="hidden" class="answer_info" name="${qnum}_answer_info_${inputedMcqAnswersDiv.dataset.counter}"/>
                <div class="add-delete-btns">
                    <button type="button" class="btn btn-warning mcq-status mcq-false exempt">False</button>
                    <button  type="button" class="btn btn-danger mcq-delete exempt">delete</button>
                </div>
            `;
             }else {
                mcqAnswerDiv.innerHTML = `
                <br/>
                <div class="formatted-answer-option"></div>
                <input value="${display_value}" type="hidden" name="${qnum}_image_label_${inputedMcqAnswersDiv.dataset.counter}"/>
                <input value="${answer_info_encoding}" type="hidden" class="answer_info" name="${qnum}_answer_info_${inputedMcqAnswersDiv.dataset.counter}"/>
                <div class="add-delete-btns">
                    <button type="button" class="btn btn-warning mcq-status mcq-false exempt">False</button>
                    <button  type="button" class="btn btn-danger mcq-delete exempt">delete</button>
                </div>
            `;
            
             }
           
            // Append the formatted_answer element as a child
            var formattedAnswerDiv = mcqAnswerDiv.querySelector('.formatted-answer-option');
            formattedAnswerDiv.appendChild(formatted_answer);
            if (answer_type === 'i-answer'){
                formattedAnswerDiv.appendChild(mcqImagePreview.cloneNode(true));
                if(imageUploadInput.files.length === 0 ){
                    alert('You must select an image file');
                    throw 'Image expected to be selected but wasn\'t'
                }
                const image_input_field_clone = imageUploadInput.cloneNode(true);
                image_input_field_clone.name = `${qnum}_answer_value_${inputedMcqAnswersDiv.counter}`;
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
    //const holder =  parseInt(inputedMcqAnswersDiv.dataset.counter)
//     inputedMcqAnswersDiv.dataset.counter  = `${holder+1}`;

    return inputedMcqDiv;
}




num_questions += 1;
part_num_questions += 1;
return questionBlock;

}


/// addQuestionBlock END //////////////////////////////////////////////////////



function checkQuestionBlock(questionBlock){
        // Make sure question text is valid
        const questionTextArea = questionBlock.querySelector('.question-textarea');
        const hiddenQuestionType = questionBlock.querySelector('.hidden-q-type');
        const inputedMcqAnswersDiv = questionBlock.querySelector('.inputed-mcq-answers');
        const inputedMpAnswersDiv = questionBlock.querySelector('.inputed-mp-answers');
        const structuralAnswerInput = questionBlock.querySelector('.q-answer-hidden');
        if (questionTextArea.value.length <= 5){
            alert('A question cannot be this short!');
            return false;
        }
        const valid_textarea = validateText(questionTextArea.value, varSymbolsArray);
        if (!valid_textarea){
            alert('The question text has undefined symbol(s) in variable expression(s)');
            return false;
        }
        const selected_topic = checkTopicAndSubtopic();
        if (!selected_topic){
            alert("Please select both a topic and a subtopic.");
            return false;
        }
        if (hiddenQuestionType.value==='e-answer'){
            try{
                if(structuralAnswerInput.value.length < 1){
                    alert('You must provide an answer');
                    return false;
                }
                const userInputNode = math.simplify(processString(structuralAnswerInput.value));
                var userInputString = userInputNode.toString();
                // The following is in case we don't want to change the domain of the algebraic expression
                // for example, if we don't want (x+1)(x-1)/(x-1) to simplify to just (x+1)
                //var userInputString = math.simplify(userInputNode, {}, {context: math.simplify.realContext}).toString()
                structuralAnswerInput.value = userInputString;
    
            }catch {
                alert('Expression in answer not valid algebraic expression');
                return false;
            }
    
        }
        else if(
            hiddenQuestionType.value==='f-answer'
        ) {
            try{
                const userInputNode = math.simplify(processString(structuralAnswerInput.value));
                var userInputString = userInputNode.evaluate();
                if(typeof(userInputString) != 'number'){
                    alert('You selected float mode but the answer you provided is not a float');
                    return false;
                }
                structuralAnswerInput.value = userInputString;
            }catch {
                if(!validateText(structuralAnswerInput.value, varSymbolsArray, isFloat=true)){
                    alert('You selected float mode but the answer you provided is not a float\
                        \n or You have undefined variable(s) in expression you entered.');
                    return false;
                    }
            }
            
            
        } else if (hiddenQuestionType.value=='m-answer'){
            if(inputedMcqAnswersDiv.dataset.counter  < 2){
                alert('The number of options for an MCQ must be at least 2.');
                return false;
            }
            if(inputedMcqAnswersDiv.dataset.trueCounter  < 1){
                alert('Must select at least one MCQ answer as correct.');
                return false;
            }
        } else if(hiddenQuestionType.value=='mp-answer'){
            if(inputedMpAnswersDiv.dataset.mereCounter < 2){
                alert('You must enter at least two matching pairs');
                return false
            }else {
                const nodeP = document.createElement('p');
                const mpnum = `<input type='hidden' value=${inputedMpAnswersDiv.dataset.mereCounter + 1} name="${inputedMpAnswersDiv.dataset.qnumber}_num_of_mps"/>`
                nodeP.innerHTML = mpnum
                questionBlock.appendChild(nodeP);
            }

        } else if(hiddenQuestionType.value==='none'){
            alert('You must enter an answer');
            return false;
        }
    
    return true
}




// --------------------------SETTINGS -------------------------------------------//

const settingsIcon = document.querySelector('.settings-icon');
const settingsSection = document.querySelector('.question-settings');
const settingsXBtn = settingsSection.querySelector('#close-x-settings');

settingsXBtn.addEventListener('click', (event)=>{
    event.preventDefault();
    settingsSection.classList.add('hide');
  })
  
  settingsIcon.addEventListener('click', (event)=>{
    event.preventDefault();
    settingsSection.classList.remove('hide');
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  })






});


  
