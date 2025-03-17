import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [profile, setProfile] = useState('');
  const [gaps, setGaps] = useState(null);

  const handleProfileChange = (event) => {
    setProfile(event.target.value);
  };

  const handleProfileSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/profile_analysis', {
        profile: profile
      });
      setGaps(response.data);
    } catch (error) {
      console.error('Error analyzing profile:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>LinkedIn Job Gap Analyzer</h1>
        <a href="http://localhost:5000/login">Login with LinkedIn</a>
      </header>
      <main>
        <form onSubmit={handleProfileSubmit}>
          <label>
            LinkedIn Profile URL:
            <input type="text" value={profile} onChange={handleProfileChange} />
          </label>
          <button type="submit">Analyze Profile</button>
        </form>
        {gaps && (
          <div className="gaps">
            <h2>Profile Gaps Analysis</h2>
            <table>
              <thead>
                <tr>
                  <th>Category</th>
                  <th>Missing in Profile</th>
                  <th>Frequency in Jobs</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Skills</td>
                  <td>{gaps.skills_gap.join(', ')}</td>
                  <td>85%, 70%</td>
                </tr>
                <tr>
                  <td>Certifications</td>
                  <td>{gaps.certification_gap.join(', ')}</td>
                  <td>65%</td>
                </tr>
                <tr>
                  <td>Experience</td>
                  <td>{gaps.experience_gap.join(', ')}</td>
                  <td>55%</td>
                </tr>
                <tr>
                  <td>Education</td>
                  <td>{gaps.education_gap.join(', ')}</td>
                  <td>50%</td>
                </tr>
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;