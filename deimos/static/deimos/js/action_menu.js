document.addEventListener('DOMContentLoaded',()=>{

 const menuToggle = document.querySelector('.menuToggle');
if (menuToggle != null){
    menuToggle.addEventListener('click', (event)=>{
        event.preventDefault();
        menuToggle.classList.toggle('active');
    }) 
}

})

