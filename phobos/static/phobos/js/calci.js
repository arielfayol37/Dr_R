const screen=document.querySelector('#screen');
var btn=document.querySelectorAll('.calc-btn');
var previousActiveElement = document.activeElement;
var trigMode = 'deg'; //deg by default
const degModeBtn = document.querySelector('#deg-mode');
degModeBtn.classList.add('active');
const logBtn = document.querySelector(".logarithm-btn");
const radModeBtn = document.querySelector('#rad-mode');
var cursorPosition = screen.selectionStart;

const invBtn = document.querySelector('#inv-mode');
const trigBtns = document.querySelectorAll('.trig');
const specialBtns = document.querySelectorAll('.special');


/////// CODE COPIED FROM https://mathjs.org/examples/browser/angle_configuration.html.html /////

let replacements = {}

// our extended configuration options
const config = {
  angles: 'deg' // 'rad', 'deg', 'grad'
}

// create trigonometric functions replacing the input depending on angle config
const fns1 = ['sin', 'cos', 'tan', 'sec', 'cot', 'csc']
fns1.forEach(function(name) {
  const fn = math[name] // the original function

  const fnNumber = function (x) {
    // convert from configured type of angles to radians
    switch (config.angles) {
      case 'deg':
        return fn(x / 360 * 2 * Math.PI)
      case 'grad':
        return fn(x / 400 * 2 * Math.PI)
      default:
        return fn(x)
    }
  }

  // create a typed-function which check the input types
  replacements[name] = math.typed(name, {
    'number': fnNumber,
    'Array | Matrix': function (x) {
      return math.map(x, fnNumber)
    }
  })
})

// create trigonometric functions replacing the output depending on angle config
const fns2 = ['asin', 'acos', 'atan', 'atan2', 'acot', 'acsc', 'asec']
fns2.forEach(function(name) {
  const fn = math[name] // the original function

  const fnNumber = function (x) {
    const result = fn(x)

    if (typeof result === 'number') {
      // convert to radians to configured type of angles
      switch(config.angles) {
        case 'deg':  return result / 2 / Math.PI * 360
        case 'grad': return result / 2 / Math.PI * 400
        default: return result
      }
    }

    return result
  }

  // create a typed-function which check the input types
  replacements[name] = math.typed(name, {
    'number': fnNumber,
    'Array | Matrix': function (x) {
      return math.map(x, fnNumber)
    }
  })
})

// import all replacements into math.js, override existing trigonometric functions
math.import(replacements, {override: true})


////// END OF COPIED CODE ///////////////
const replacementDict = {
  'e+':'e^',
  'e-':'e^-',
  'π':'pi',
  '√':'sqrt',
  'log':'log10', // MathJS assumes natural log by default.
  'ln':'log'// maybe order matters here. ln should be after log I think.
}

const specialBtnsTextDict ={
      'x y':'^',
      '√':  '√',
      'log': 'log',
      'sin':'sin',
      'asin':'asin',
      'cos':'cos',
      'acos':'acos',
      'tan':'tan',
      'atan':'atan',
      'ln':'ln'
        
}
document.addEventListener('DOMContentLoaded', ()=>{


    
    /*============ For getting the value of btn, Here we use for loop ============*/
    for(item of btn)
    {   
      if(!item.classList.contains('exempt')){
            item.addEventListener('click',(e)=>{
              const inputEvent = new Event('input', {
             bubbles: true,
             cancelable: true,
        });
        screen.dispatchEvent(inputEvent);

              
                btntext=e.target.innerText;
                screen.focus();
                cursorPosition = screen.selectionStart;
                if(btntext =='×')
                {
                    btntext= '*';
                }
        
                if(btntext=='÷')
                {
                    btntext='/';
                }
                if(btntext=='x!')
                {
                    btntext='!';
                }
                
                if (previousActiveElement === screen) {
                    // If the screen has focus, add text at the cursor position
                    
                    const textBeforeCursor = screen.value.substring(0, cursorPosition);
                    const textAfterCursor = screen.value.substring(cursorPosition);
                    screen.value = textBeforeCursor + btntext + textAfterCursor;
                    
                    
                  } else {
                    // If the screen doesn't have focus, add text at the end
                    screen.value += btntext;
                  }
                  cursorPosition += btntext.length;
                  screen.setSelectionRange(cursorPosition, cursorPosition); // Move the cursor after the added text

                }
                );
    
              } 
        
    }

    degModeBtn.addEventListener('click', () => {
        radModeBtn.classList.remove('active'); // Remove 'active' class from the other button
        degModeBtn.classList.add('active'); // Add 'active' class to the clicked button
        trigMode = 'deg';
        config.angles = 'deg';
        const event = new Event('input');
        screen.dispatchEvent(event);
      });
      
      radModeBtn.addEventListener('click', () => {
        degModeBtn.classList.remove('active'); // Remove 'active' class from the other button
        radModeBtn.classList.add('active'); // Add 'active' class to the clicked button
        trigMode = 'rad';
        config.angles = 'rad';
        const event = new Event('input');
        screen.dispatchEvent(event);
      });
      
      screen.addEventListener('focus',()=>
      {
        previousActiveElement = screen;
      })



      /* Special BUTTONS */
      specialBtns.forEach((item)=>{
        item.addEventListener('click',()=>{
            screen.value += `${specialBtnsTextDict[item.textContent.trim()]}()`
            screen.focus();
            cursorPosition = screen.value.length - 1;
            screen.setSelectionRange(cursorPosition, cursorPosition); 
        })
      }
      )



      invBtn.addEventListener('click', ()=>{
        for(item of trigBtns){

           if(item.textContent.startsWith('a')){
            item.textContent = item.textContent.slice(1);
           } else{
            item.textContent = `a${item.textContent}`
           }
          }
          if(logBtn.textContent === 'ln'){
            logBtn.textContent = 'log'
          }else {
            logBtn.textContent = 'ln'
          }
      })

      
    

});


function backspc()
{
    screen.value=screen.value.substr(0,screen.value.length-1);
}
function mathjsEval(){
    const output = math.parse(processString(screen.value)).evaluate();
    screen.value = `${output}`;
    screen.focus();
    cursorPosition = screen.value.length;
    screen.setSelectionRange(cursorPosition, cursorPosition);
}

function replaceChars(str, charA, charB) {
    const regex = new RegExp(charA, 'g'); // 'g' flag for global replacement
    return str.replace(regex, charB);
  }


  function processString(str) {
    let result = str;
  
    for (const charA in replacementDict) {
      const charB = replacementDict[charA];
      const regex = new RegExp(charA, 'g');
      result = result.replace(regex, charB);
    }
    result = transformExpression(result)
    //console.log(result);
    return result;
  }

  
  function transformExpression(expr) {
    let expression = removeExtraSpacesAroundOperators(expr);
    // !Important, the order of these functions is crucial!
    const trigFunctions = {
        'asin': 'ò', 'acos': 'ë', 'atan': 'à', 'arcsin': 'ê', 'arccos': 'ä',
        'arctan': 'ï', 'sinh': 'ù', 'cosh': 'ô', 'tanh': 'ü', 'sin': 'î', 'cos': 'â', 
        'tan': 'ö', 'log': 'ÿ', 'ln': 'è',
        'cosec': 'é', 'sec': 'ç', 'cot': 'û', 'sqrt':'у́', 'pi': 'я',
    };

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
        (/[a-zA-Z]/.test(char) || Object.values(trigFunctions).includes(char)) && /\w/.test(prevChar) ||
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
