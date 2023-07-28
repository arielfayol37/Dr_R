document.getElementById('topicSelect').addEventListener('change', function() {

    var selectedTopic = this.value;
    var subTopicSelect = document.getElementById('subTopicSelect');
    
    // Hide the subTopicSelect if no topic is selected
    if (selectedTopic === '') {
      subTopicSelect.style.display = 'none';
      return;
    }
    
    // Fetch subtopics for the selected topic from the Django view
    fetch(`get_subtopics/${encodeURIComponent(selectedTopic)}`)
      .then(response => response.json())
      .then(data => {
        // Populate the subTopicSelect with the fetched subtopics
        subTopicSelect.innerHTML = '';
        data.subtopics.forEach(function(subTopic) {
          var option = document.createElement('option');
          option.textContent = subTopic;
          option.value = subTopic;
          subTopicSelect.appendChild(option);
        });
        
        // Display the subTopicSelect
        subTopicSelect.style.display = 'inline';
      })
      .catch(error => {
        console.error('Error fetching subtopics:', error);
      });
  });