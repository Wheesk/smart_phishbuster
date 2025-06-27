chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url.startsWith('http')) {
    // Send URL to content script
    chrome.tabs.sendMessage(tabId, { type: 'NEW_URL', url: tab.url });
  }
});
