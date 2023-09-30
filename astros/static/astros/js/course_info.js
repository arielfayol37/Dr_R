
document.querySelector('.info_body').addEventListener('click',(event)=>{
    event.preventDefault();
    target_ = event.target;
    
    if(target_.classList.contains('expand')){
        Body= target_.parentNode.parentNode.parentNode.querySelector('.body-text')
        console.log(Body)
        if(!target_.innerHTML.classList.contains('open')){
        Body.style.display='block';
        target_.classList.add('open');
        }
        else{
            Body.style.display='none';
        target_.classList.remove('open');
        }
    }
    else if(target_.classList.contains('head')){
        Body= target_.parentNode.querySelector('.body-text')
        console.log(Body)
        if(!target_.querySelector('.expand').classList.contains('open')){
        Body.style.display='block';
        target_.querySelector('.expand').classList.add('open');
        }
        else{
            Body.style.display='none';
        target_.querySelector('.expand').classList.remove('open');
        }

    }
    else if(target_.parentNode.classList.contains('head')){
        Body= target_.parentNode.parentNode.querySelector('.body-text')
        console.log(Body)
        if(!target_.querySelector('.expand').classList.contains('open')){
        Body.style.display='block';
        target_.querySelector('.expand').classList.add('open');
        }
        else{
            Body.style.display='none';
        target_.querySelector('.expand').classList.remove('open');
        }

    }
})



