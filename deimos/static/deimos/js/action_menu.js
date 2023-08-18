let menuToggle = document.querySelector('.menuToggle');
menuToggle.addEventListener('click', (event)=>{
    event.preventDefault();
    menuToggle.classList.toggle('active');
})