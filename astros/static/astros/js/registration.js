
document.addEventListener('DOMContentLoaded',()=>{
const submitBtns = document.querySelectorAll('.submit-btn-register');

// Blurring out depending on the selected side

// Select both registration forms
const phobosForm = document.querySelector('.register-phobos');
const deimosForm = document.querySelector('.register-deimos');

// Event listener for when an input inside the phobosForm is focused
phobosForm.addEventListener('focusin', function() {
    deimosForm.classList.add('blur');
});

// Event listener for when an input inside the phobosForm is blurred (loses focus)
phobosForm.addEventListener('focusout', function() {
    if (!isAnyInputFocused(phobosForm)) {
        deimosForm.classList.remove('blur');
    }
});

// Same for deimosForm
deimosForm.addEventListener('focusin', function() {
    phobosForm.classList.add('blur');
});

deimosForm.addEventListener('focusout', function() {
    if (!isAnyInputFocused(deimosForm)) {
        phobosForm.classList.remove('blur');
    }
});

// Helper function to check if any input inside the given parent is focused
function isAnyInputFocused(parent) {
    return Array.from(parent.querySelectorAll('input')).some(input => input === document.activeElement);
}

submitBtns.forEach((submitBtn)=>{
    submitBtn.addEventListener('click', (event)=>{
    event.preventDefault();
    const form = submitBtn.closest('.registration-form');    
    const emailField = form.querySelector('[name="email"]');
    const passwordField = form.querySelector('[name="password"]');
    const confirmPasswordField = form.querySelector('[name="confirmation"]');
    const authenticationArea = form.querySelector('.authentication-area');
        console.log(emailField.value)
    // Clear previous error messages
    clearErrorMessages(form);

    if (!isValidEmail(emailField.value)) {
        displayErrorMessage(emailField, "Invalid email address.");

        return;
    }

    if (!isValidPassword(passwordField.value, confirmPasswordField.value)) {
        if (passwordField.value.length < 8) {
            displayErrorMessage(passwordField, "Password should be at least 8 characters long.");
        }
        if (passwordField.value !== confirmPasswordField.value) {
            displayErrorMessage(confirmPasswordField, "Passwords do not match.");
        }
        return;
    }

    if(authenticationArea.classList.contains('closed')){
        fetch('/authentification/generate_code', {
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            body: JSON.stringify({
                    email: emailField.value
            })
          })
          .then(response => response.json())
          .then(result => {
              alert(result.message);
              if(result.success){
                authenticationArea.style.display='block';
                authenticationArea.classList.remove('closed');
              }
          });
    }else {
        fetch('/authentification/validate_code', {
            method: 'POST',
            headers: { 'X-CSRFToken': getCookie('csrftoken') },
            body: JSON.stringify({
                    code: authenticationArea.querySelector('.input-code').value,
                    email: emailField.value
                    
            })
          })
          .then(response => response.json())
          .then(result => {
              alert(result.message);
              if(result.success){
                form.querySelector('form').submit();
              }
          })
    }


    })
})


// Helper function to check email validity using a simple regex pattern
function isValidEmail(email) {
    const regex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
    return regex.test(email);
}

// Helper function to check password validity
function isValidPassword(password, confirmPassword) {
    if (password.length < 8 || password !== confirmPassword) {
        return false;
    }
    return true;
}

// Helper function to display error message above input
function displayErrorMessage(inputElement, message) {
    const errorMessage = document.createElement('div');
    errorMessage.className = 'input-error-message';
    errorMessage.innerText = message;
    inputElement.parentElement.insertBefore(errorMessage, inputElement);
}

// Helper function to clear error messages from the form
function clearErrorMessages(form) {
    const errorMessages = form.querySelectorAll('.input-error-message');
    errorMessages.forEach(errorMessage => errorMessage.remove());
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

})
