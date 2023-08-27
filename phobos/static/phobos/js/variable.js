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
    