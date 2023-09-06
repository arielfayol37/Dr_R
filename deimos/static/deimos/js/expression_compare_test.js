
document.addEventListener('DOMContentLoaded', ()=>{
    const yellowLight = document.querySelector('.yellow-light');
    const greenLight = document.querySelector('.green-light');
    const redLight = document.querySelector('.red-light');
    const compareBtn = document.querySelector('.compare-btn');
    const e1Field = document.querySelector('.e1-field');
    const e2Field = document.querySelector('.e2-field');
    const replacementDict = {
        'π':'pi',
        '√':'sqrt'
    }
    var e1_toBeCompared, e2_toBeCompared;
    compareBtn.addEventListener('click', (event)=>{
        event.preventDefault();
        if(e1Field.value.length === 0 || e2Field.value.length ===0){
            alert('Cannot compare blank expression(s)')
            return;
        }else{
            try{
                e1_toBeCompared = math.simplify(processString(e1Field.value)).toString();
                e2_toBeCompared = math.simplify(processString(e2Field.value)).toString();
                //console.log(e1_toBeCompared);
                //console.log(e2_toBeCompared);
            }catch{
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
                    expression_2: e2_toBeCompared   
            })
          })
          .then(response => response.json())
          .then(result => {
              toggleLight(result.correct,too_many_attempts=false,redLight,yellowLight,greenLight);
          });

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



  function processString(str) {
    let result = str;
  
    for (const charA in replacementDict) {
      const charB = replacementDict[charA];
      const regex = new RegExp(charA, 'g');
      result = result.replace(regex, charB);
    }
  
    return result;
  }
})