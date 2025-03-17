document.getElementById('login').addEventListener('click', () => {
  chrome.runtime.sendMessage({ action: 'login' }, (response) => {
    if (response.success) {
      document.getElementById('output').innerText = 'Logged in successfully!';
    } else {
      document.getElementById('output').innerText = 'Failed to log in.';
    }
  });
});

document.getElementById('analyze').addEventListener('click', () => {
  chrome.runtime.sendMessage({ action: 'analyzeProfile' }, (response) => {
    if (response.gaps) {
      document.getElementById('output').innerText = JSON.stringify(response.gaps, null, 2);
    } else {
      document.getElementById('output').innerText = 'Failed to analyze profile.';
    }
  });
});

document.getElementById('recommend').addEventListener('click', () => {
  chrome.runtime.sendMessage({ action: 'getRecommendations' }, (response) => {
    if (response.recommendations) {
      document.getElementById('output').innerText = JSON.stringify(response.recommendations, null, 2);
    } else {
      document.getElementById('output').innerText = 'Failed to get recommendations.';
    }
  });
});