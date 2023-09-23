document.addEventListener('DOMContentLoaded', () => {
    const assignBtn = document.querySelector('.assign-btn');
    assignBtn.addEventListener('click', () => {
        // Implement the fetch.
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
            if (data.success) {
                assignBtn.parentNode.removeChild(assignBtn);
            }
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
    });
});
