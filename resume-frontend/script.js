fetch('https://4z6q985fyj.execute-api.us-west-1.amazonaws.com/staging', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
})
.then(response => {
    if (!response.ok) {
        throw new Error('Failed to trigger Lambda function');
    }
    return response.json(); // Parse the response body as JSON
})
.then(data => {
    // Access the returned value from the API response
    const newValue = data.value;

    // Update the counter on the HTML page with the new value
    document.getElementById('viewCount').innerText = `View Count: ${newValue}`;
})
.catch(error => {
    console.error('Error:', error);
});
