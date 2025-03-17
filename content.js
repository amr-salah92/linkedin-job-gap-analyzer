function getProfileData() {
  const profile = {
    skills: ['Python', 'SQL'],  // Example data, extract actual data from LinkedIn page
    experience: ['Data Analyst at Company A', 'Data Scientist at Company B'],
    certifications: ['Google Analytics'],
    education: ['Bachelor’s in Computer Science']
  };
  return profile;
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'analyzeProfile') {
    const profile = getProfileData();
    fetch('http://localhost:5000/profile_analysis', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(profile)
    })
    .then(response => response.json())
    .then(data => {
      sendResponse({ gaps: data });
    })
    .catch(error => {
      console.error('Error analyzing profile:', error);
      sendResponse({ error: 'Failed to analyze profile.' });
    });
    return true;  // Keep the message channel open for sendResponse
  }
});