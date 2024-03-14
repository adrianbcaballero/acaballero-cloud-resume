fetch('https://r05eb4w5b0.execute-api.us-west-1.amazonaws.com/dev/proxy', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
})
.then(response => {
    if (!response.ok) {
        throw new Error('Failed to trigger Lambda function');
    }
    return response.json(); 
})
.then(data => {
    console.log('Response data:', data);
    const parsedBody = JSON.parse(data.body); 
    const newValue = parsedBody.value; 
  
    document.getElementById('viewCount').innerText = `View Count: ${newValue}`;
})
.catch(error => {
    console.error('Error:', error);
});
