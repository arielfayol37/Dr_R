
    document.addEventListener('DOMContentLoaded', function() {
        const form = document.querySelector('.info-form');
        const categoryBtns = document.querySelectorAll('.c-btn');
        const textInfo = form.querySelector('.textarea-info');  
        const category = form.querySelector('.input-category');
        const infoEditBtn = document.querySelector('.info-edit-btn');
        const formattedInfo = document.querySelector('.formatted-answer-option');
        const cancelBtn = document.querySelector('.cancel-btn');
        var previousBtn = document.querySelector('.abc-btn');

        infoEditBtn.addEventListener('click', (event)=>{
            event.preventDefault();
            infoEditBtn.style.display = 'none';
            formattedInfo.style.display = 'none'
            form.style.display = 'block';
            textInfo.value = previousBtn.dataset.info;
            textInfo.scrollIntoView({ behavior:"smooth" })
        })

        cancelBtn.addEventListener('click', (event)=>{
            event.preventDefault();
            formattedInfo.style.display = 'block';
            infoEditBtn.style.display = 'block';
            form.style.display = 'none';
        })
        textInfo.value = previousBtn.dataset.info
        categoryBtns.forEach((btn)=>{
            btn.addEventListener('click', (event)=>{
                event.preventDefault();
                formattedInfo.style.display = 'block';
                formattedInfo.innerHTML = btn.dataset.md;
                category.value = btn.dataset.category;
                btn.classList.add('active');
                previousBtn.classList.remove('active');
                previousBtn = btn;
                textInfo.value = previousBtn.dataset.info
            })
        })

        form.addEventListener('submit', function(event) {
            event.preventDefault();
                  
            fetch('save_course_info', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                   // 'X-CSRFToken': '{{ csrf_token }}',
                },
                body: JSON.stringify({
                    text_info: textInfo.value,
                    category: category.value,
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    infoEditBtn.style.display = 'block';
                    form.style.display = 'none';
                    previousBtn.dataset.md = data.md;
                    previousBtn.dataset.info = textInfo.value
                    formattedInfo.innerHTML = data.md;
                    formattedInfo.style.display = 'block';
                    alert(data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

