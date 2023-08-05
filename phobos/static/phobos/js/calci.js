var screen=document.querySelector('#screen');
var btn=document.querySelectorAll('.btn');
var previousActiveElement = document.activeElement;
var trigMode = 'deg'; //deg by default
const degModeBtn = document.querySelector('#deg-mode');
degModeBtn.classList.add('active');

const radModeBtn = document.querySelector('#rad-mode');
var cursorPosition = screen.selectionStart;

const invBtn = document.querySelector('#inv-mode');
const trigBtns = document.querySelectorAll('.trig');
const specialBtns = document.querySelectorAll('.special');

const replacementDict = {
    'π':'pi',
    '√':'sqrt'
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
      'atan':'atan'
        
}
document.addEventListener('DOMContentLoaded', ()=>{


    
    /*============ For getting the value of btn, Here we use for loop ============*/
    for(item of btn)
    {
        if(!item.classList.contains('exempt')){
            item.addEventListener('click',(e)=>{
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

                });
    
        }
        
    }

    degModeBtn.addEventListener('click', () => {
        radModeBtn.classList.remove('active'); // Remove 'active' class from the other button
        degModeBtn.classList.add('active'); // Add 'active' class to the clicked button
        trigMode = 'deg';
      });
      
      radModeBtn.addEventListener('click', () => {
        degModeBtn.classList.remove('active'); // Remove 'active' class from the other button
        radModeBtn.classList.add('active'); // Add 'active' class to the clicked button
        trigMode = 'rad';
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
  
    return result;
  }