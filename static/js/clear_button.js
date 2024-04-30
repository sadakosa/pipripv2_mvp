document.getElementById('clear_button').addEventListener('click', function() {
    fetch('/clear_db', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.ok) {
            console.log('Cleared DB successfully.');
            setTimeout(() => location.reload(), 100);
        } else {
            console.error('Error clearing DB:', response.statusText);
        }
    })
    .catch(error => console.error('Error:', error));
});