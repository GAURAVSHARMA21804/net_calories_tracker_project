document.getElementById('signup-form').addEventListener('submit', function(e) {
    e.preventDefault();  // Prevent the default form submission

    const formData = new FormData(this);

    // Convert FormData to a JSON object
    const jsonData = {};
    formData.forEach((value, key) => {
        jsonData[key] = value;
    });

    fetch("{% url 'users_auth:signup' %}", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',  // Specify JSON content type
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: JSON.stringify(jsonData),  // Send JSON-formatted data
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            // Store JWT tokens in localStorage
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);

            // Redirect to the user dashboard after signup
            window.location.href = '/dashboard/';  // Or wherever you want to redirect
        }
    })
    .catch(error => console.error('Error:', error));
});
