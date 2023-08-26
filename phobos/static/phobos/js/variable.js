document.addEventListener('DOMContentLoaded', ()=>{

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
            varInfoDiv.style.display = 'block';
        }
        else if(state==='open'){
            state ='closed';
            varInfoDiv.style.display = 'none';
        }
    })
    
    varInfoDiv.addEventListener('click', (event)=>{
        event.preventDefault();
        if(event.target.classList.contains('btn-create-var')){
            const varSymbolField = varInfoDiv.querySelector('.var-symbol');
            const varDomainField = varInfoDiv.querySelector('.var-domain');
            symbol = varSymbolField.value;
            if (symbol.length === 0 ){
                alert('You must enter a symbol');
                return;
            } else if ((symbol.length > 3) || (symbol.length === 2) || (/^[a-zA-Z]$/.test(symbol.charAt(0)) === false) || 
            ((symbol.charAt(1) != '_') && (symbol.length===3))){
                alert('Invalid symbol');
                return;
            }
            enteredDomain = varDomainField.value;
            var parsedDomain = parseDomainInput(enteredDomain);
            if(parsedDomain.length === 0){
                alert('Invalid domain');
                return;
            }

            // passed all the tests

            const newVarDiv = document.createElement('div');
            newVarDiv.innerHTML = symbol;
            // TODO: add the hidden input fields.
            createdVarsDiv.appendChild(newVarDiv);
            varInfoDiv.style.display = 'none';
            varSymbolField.value = '';
            varDomainField.value = '';

        }

    })

})


        function parseDomainInput(input) {
            const boundsArray = [];
            const groups = input.match(/\((.*?)\)/g); // Match text within parentheses

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
    