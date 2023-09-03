document.addEventListener('DOMContentLoaded',()=>{
    // tol == triple-orange-line
    const tol = document.querySelector('#triple-orange-lines');
    const sidebarDiv = document.querySelector('.sidebar');
    const sidebarX = document.querySelector('.sidebar-header');
    tol.addEventListener('click', (event)=>{
        event.preventDefault();
        //const top = tol.getBoundingClientRect().top
        sidebarDiv.style.top = `${40}px`
        sidebarDiv.style.display = 'block';


    })
    sidebarX.addEventListener('click', ()=> {
        sidebarDiv.style.display = 'none';
    })
})