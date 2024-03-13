fetch('https://adriancaballeroresume.com/staging', {
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
    const newValue = data.value;

    document.getElementById('viewCount').innerText = `View Count: ${newValue}`;
})
.catch(error => {
    console.error('Error:', error);
});
