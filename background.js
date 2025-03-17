chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'login') {
    chrome.tabs.create({ url: 'http://localhost:5000/login' }, (tab) => {
      chrome.tabs.onUpdated.addListener(function listener(tabId, changeInfo, tab) {
        if (tabId === tab.id && changeInfo.status === 'complete') {
          chrome.tabs.onUpdated.removeListener(listener);
          sendResponse({ success: true });
        }
      });
    });
    return true;  // Keep the message channel open for sendResponse
  } else if (request.action === 'analyzeProfile') {
    chrome.tabs.executeScript({
      code: 'document.body.innerText'
    }, (result) => {
      const profile = result[0];
      fetch('http://localhost:5000/profile_analysis', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ profile })
      })
      .then(response => response.json())
      .then(data => sendResponse({ gaps: data }))
      .catch(error => sendResponse({ error: 'Failed to analyze profile.' }));
    });
    return true;  // Keep the message channel open for sendResponse
  } else if (request.action === 'getRecommendations') {
    fetch('http://localhost:5000/recommendations', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => sendResponse({ recommendations: data }))
    .catch(error => sendResponse({ error: 'Failed to get recommendations.' }));
    return true;  // Keep the message channel open for sendResponse
  }
});