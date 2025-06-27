chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.type === 'NEW_URL') {
    fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url: msg.url })
    })
    .then(res => res.json())
    .then(data => {
      // Save result to chrome.storage for popup
      chrome.storage.local.set({ lastResult: data });
      // Optionally update badge
      chrome.action.setBadgeText({ text: data.result === 'phishing' ? '⚠️' : '' });
    })
    .catch(err => console.error('API error', err));
  }
});
