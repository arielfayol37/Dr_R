document.addEventListener('input', function (e) {
    if (e.target.tagName.toLowerCase() === 'textarea') {
        autoExpand(e.target);
    }
});

function autoExpand(textarea) {
    // Reset the height to a small value to correctly calculate the scroll height
    textarea.style.height = 'auto';
    // Set the scroll height as the new height of the textarea
    textarea.style.height = textarea.scrollHeight + 'px';
}