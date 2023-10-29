document.addEventListener('DOMContentLoaded', ()=>{
    const sideInfosIcons = document.querySelectorAll('.side-info-icon');
    const sideInfox = document.querySelectorAll('.side-info-x');

    sideInfox.forEach((Xbtn)=>{
        Xbtn.addEventListener('click', (event)=>{
          event.preventDefault();
          const sideDiv = Xbtn.closest('.side');
          sideDiv.querySelector('.side-info').classList.add('hide');
        })
      })
      var sideCounters = 0
      sideInfosIcons.forEach((sideInfoIcon)=>{
      sideInfoIcon.style.top = `${70 + 8*sideCounters}%`
      sideCounters += 1;
      sideInfoIcon.addEventListener('click', (event)=>{
        event.preventDefault();
        const sideDiv = sideInfoIcon.closest('.side');
        sideDiv.querySelector('.side-info').classList.remove('hide');
        window.scrollTo({
          top: 0,
          behavior: 'smooth'
        });
      })
      })





      const selectElement = document.getElementById('gradingSchemeSelect'); // Get the select element by its id
      var previousOptionIndex = 0;
      selectElement.addEventListener('change', function(event) { // Add an event listener for the "change" event
          const selectedValue = event.target.value; // Get the value of the selected option
          const selectedOption = event.target.options[event.target.selectedIndex];
          if (selectedValue === 'new-gs') { // Check if the selected value is "new-gs"
            // console.log("New grading scheme creating selected");
          }
          
          document.querySelector(`[data-index="${previousOptionIndex}"]`).style.display = 'none';
          previousOptionIndex = selectedOption.dataset.optionIndex;
          document.querySelector('input[name="grading_scheme_pk"]').value = previousOptionIndex;
          document.querySelector(`[data-index="${previousOptionIndex}"]`).style.display = 'flex';

      });
})
