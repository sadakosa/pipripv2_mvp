document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('input_form');
    var submitButton = form.querySelector('button[type="submit"]');
    var progressText = document.getElementById('progress_text');

    form.addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the default form submission behavior
        form.disabled = true;
        submitButton.disabled = true;
        progressText.innerText = 'Building graph... This may take more than a minute.';
        progressText.style.display = 'block';  // Display the progress text

        // Send an AJAX request to the server
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/process_input', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                progressText.innerText = 'Completed.';
                form.disabled = false;
                submitButton.disabled = false;
                setTimeout(() => location.reload(), 1000);
            } else if (xhr.readyState === 4 && xhr.status !== 200) {
                console.error('Error:', xhr.status);
                progressText.innerText = 'Error occurred.';
            }
        };
        xhr.send(new URLSearchParams(new FormData(form)));
    });
});
