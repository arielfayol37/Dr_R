
document.addEventListener('DOMContentLoaded', ()=>{
    const yellowLight = document.querySelector('.yellow-light');
    const greenLight = document.querySelector('.green-light');
    const redLight = document.querySelector('.red-light');
    const compareBtn = document.querySelector('.compare-btn');
    const e1Field = document.querySelector('.e1-field');
    const e2Field = document.querySelector('.e2-field');
    const modeBtn = document.querySelector('.mode-btn');
    const formattedDiv1 = document.querySelector('#e1');
    const formattedDiv2 = document.querySelector('#e2');
    const replacementDict = {
        'π':'pi',
        '√':'sqrt'
    }
    var e1_toBeCompared, e2_toBeCompared, e1_simplified, e2_simplified, e1_latex, e2_latex, is_units;
    is_units = false;
    modeBtn.addEventListener('click', ()=>{
      if(modeBtn.innerHTML==='expressions'){
        modeBtn.innerHTML = 'units'
        is_units = true
        e1Field.placeholder = 'Enter units 1 here';
        e2Field.placeholder = 'Enter units 2 here';
      }else{
        modeBtn.innerHTML = 'expressions'
        e1Field.placeholder = 'Enter expression 1 here';
        e2Field.placeholder = 'Enter expression 2 here';
        is_units = false
      }
      
    })
    compareBtn.addEventListener('click', (event)=>{
        event.preventDefault();
        if(e1Field.value.length === 0 || e2Field.value.length ===0){
            alert('Cannot compare blank expression(s)')
            return;
        }else{
            try{
                console.log(is_units)
                e1_simplified =  math.simplify(processString(e1Field.value, is_units))
                e2_simplified = math.simplify(processString(e2Field.value, is_units))
                e1_toBeCompared = e1_simplified.toString();
                e2_toBeCompared = e2_simplified.toString();

                console.log(e1_toBeCompared);
                console.log(e2_toBeCompared);
            }catch(error){
                //console.log(error);
                alert('Expression(s) not valid algebraic expression');
                return;
            }
            resetLightsToRed(redLight,yellowLight,greenLight);
            scrollToCenter(redLight);
            yellowLight.classList.add('activated');
            yellowLight.classList.add('blinking');
            redLight.classList.remove('activated');
            fetch(window.location.href, {
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            body: JSON.stringify({
                    expression_1: e1_toBeCompared,
                    expression_2: e2_toBeCompared,
                    mode: modeBtn.innerHTML
            })
          })
          .then(response => response.json())
          .then(result => {
              toggleLight(result.correct,too_many_attempts=false,redLight,yellowLight,greenLight);
          });

        }

    })


e1Field.addEventListener('input', ()=>{
  if(e1Field.value.length != 0){
    MathJax.typesetPromise().then(() => {
      try {
      e1_simplified = math.simplify(processString(e1Field.value, is_units))  
      e1_latex = e1_simplified.toTex();
      const formattedAnswer = MathJax.tex2chtml(e1_latex + '\\phantom{}');
      formattedDiv1.innerHTML = '';
      formattedDiv1.appendChild(formattedAnswer);
      MathJax.typesetPromise();
      } catch (error) {
        // console.log(error);
      }
      
      }); 
  }else {
    formattedDiv1.innerHTML = '';
  }

})

e2Field.addEventListener('input', ()=>{
  if(e2Field.value.length != 0){

    MathJax.typesetPromise().then(() => {
      try {
      e2_simplified = math.simplify(processString(e2Field.value, is_units))  
      e2_latex = e2_simplified.toTex();
      const formattedAnswer = MathJax.tex2chtml(e2_latex + '\\phantom{}');
      formattedDiv2.innerHTML = '';
      formattedDiv2.appendChild(formattedAnswer);
      MathJax.typesetPromise();
      } catch (error) {
        // console.log(error);
      }
      
      }); 
  } else {
    formattedDiv2.innerHTML = '';
  }

})
  
function toggleLight(correct, too_many_attempts,redLight, yellowLight, greenLight) {
    // Make the yellow light blink as though the program was 'thinking';

      if (correct) {
        
        setTimeout(function () {
          // Code to execute after 1.6 seconds
          yellowLight.classList.remove('activated');
          yellowLight.classList.remove('blinking');
          greenLight.classList.add('activated');
        }, 600);
    
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
          
        }, 600);
    
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



function processString(str, is_units=false) {
  let result = str;

  for (const charA in replacementDict) {
    const charB = replacementDict[charA];
    const regex = new RegExp(charA, 'g');
    result = result.replace(regex, charB);
  }

  return transformExpression(result, is_units);
}

function transformExpression(expr, is_units=false) {
  let expression = removeExtraSpacesAroundOperators(expr);
  // !Important, the order of these functions is crucial!
  if(is_units){
    var trigFunctions = {
      'cd': 'ò', 'mol': 'ë', 'Hz': 'à', 'Pa': 'ê','Wb': 'ä',
        'lx': 'Bq', 'Gy': 'ù', 'Sv': 'ô', 'kat': 'ü', 
    };
  }else {
    var trigFunctions = {
      'asin': 'ò', 'acos': 'ë', 'atan': 'à', 'arcsin': 'ê', 'arccos': 'ä',
      'arctan': 'ï', 'sinh': 'ù', 'cosh': 'ô', 'tanh': 'ü', 'sin': 'î', 'cos': 'â', 
      'tan': 'ö', 'log': 'ÿ', 'ln': 'è',
      'cosec': 'é', 'sec': 'ç', 'cot': 'û', 'sqrt':'у́', 'pi': 'я',
  };
  }


  expression = encode(expression, trigFunctions);

  let transformedExpression = [...expression].map((char, index) => {
      if (index !== 0 && needsMultiplication(expression, index, trigFunctions)) {
          return '*' + char;
      }
      return char;
  }).join('');

  return decode(transformedExpression, trigFunctions);
}

function removeExtraSpacesAroundOperators(text) {
  return text.replace(/\s*([-+*/^])\s*/g, '$1');
}

function needsMultiplication(expr, index, trigFunctions) {
  const char = expr[index];
  const prevChar = expr[index - 1];
  return (
      (/[a-zA-Z]/.test(char) || Object.values(trigFunctions).includes(char)) && (/\w/.test(prevChar) || 
      Object.values(trigFunctions).includes(prevChar))||
      /\d/.test(char) && /[a-zA-Z]/.test(prevChar) ||
      char === '(' && (/[a-zA-Z]/.test(prevChar) && !Object.values(trigFunctions).includes(prevChar))
  );
}

function encode(text, trigFunctions) {
  let result = text;
  for (let [key, value] of Object.entries(trigFunctions)) {
      result = result.replace(new RegExp(key, 'g'), value);
  }
  return result;
}

function decode(text, trigFunctions) {
  let result = text;

  for (let [key, value] of Object.entries(trigFunctions)) {
      result = result.replace(new RegExp(value, 'g'), key);
  }

  return result;
}



})