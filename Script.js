document.getElementById('predictButton').addEventListener('click', async () => {
  const messageText = document.getElementById('messageInput').value.trim();
  const resultDiv = document.getElementById('result');
  const spinner = document.getElementById('loadingSpinner');

  if (!messageText) {
    alert('Please Enter A Message!');
    return;
  }

  resultDiv.innerText = '';
  spinner.classList.remove('hidden');

  try {
    const response = await fetch('http://localhost:8000/Predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: messageText }) // FIXED: don't wrap "message" in another object.
    });

    if (!response.ok) throw new Error('Server Error');

    const data = await response.json();
    resultDiv.innerText = `${data.Prediction} (${data.Confidence}% Confidence)`;

  } catch (error) {
    resultDiv.innerText = 'Failed To Connect To The Server.';
  } finally {
    spinner.classList.add('hidden');
  }
});

document.getElementById('toggleTheme').addEventListener('click', () => {
  const html = document.documentElement;
  const currentTheme = html.getAttribute('data-theme');
  html.setAttribute('data-theme', currentTheme === 'light' ? 'dark' : 'light');
});

