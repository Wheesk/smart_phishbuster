document.addEventListener('DOMContentLoaded', () => {
  const status = document.getElementById('status');

  // 1) Get the current active tab
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const url = tabs[0]?.url;
    if (!url) {
      status.textContent = 'No active tab URL.';
      return;
    }

    // 2) Show a loading message
    status.textContent = 'Checking ' + url + ' …';

    // 3) Call your backend directly from the popup
    fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    })
    .then((res) => res.json())
    .then((data) => {
      status.innerHTML = `
        <p><strong>URL:</strong> ${data.url}</p>
        <p><strong>Result:</strong> ${data.result}</p>
        <p><strong>Score:</strong> ${data.phishing_probability}</p>
      `;
    })
    .catch((err) => {
      console.error(err);
      status.textContent = 'Error fetching verdict.';
    });
  });
});
