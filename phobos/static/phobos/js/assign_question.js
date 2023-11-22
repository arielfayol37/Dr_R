document.addEventListener('DOMContentLoaded', () => {
    const assignBtn = document.querySelector('.assign-btn');
    const preloader = document.querySelector('#preloader');
    assignBtn.addEventListener('click', () => {
        // Implement the fetch.
        preloader.classList.remove('hide');
        fetch(window.location.href + '/assign', {
            method: 'POST', 
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            preloader.classList.add('hide');
            if (data.success) {
                assignBtn.parentNode.removeChild(assignBtn);
            }
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
    });
});
