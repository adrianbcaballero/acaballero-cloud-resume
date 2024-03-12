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
    console.log('Lambda function triggered successfully');
})
.catch(error => {
    console.error('Error:', error);
});
