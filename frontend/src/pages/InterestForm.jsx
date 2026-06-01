import React, { useState } from 'react';
import { Link } from 'react-router-dom';

function InterestForm({ API }) {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    interests: [],
    mbtiType: '',
    preferences: {}
  });

  const interestOptions = [
    'Art', 'Painting', 'Music', 'Writing', 'Programming',
    'Reading', 'Cooking', 'Gardening', 'Hiking', 'Gaming',
    'Photography', 'Dance', 'Crafts', 'Science', 'Philosophy',
    'History', 'Language Learning', 'Fitness', 'Meditation',
    'Singing', 'Acting', 'DIY Projects', 'Volunteering'
  ];

  const mbtiOptions = [
    { code: 'ISTJ', description: 'The Logistician - Organized and practical' },
    { code: 'ISFJ', description: 'The Defender - Caring and responsible' },
    { code: 'INFJ', description: 'The Advocate - Insightful and imaginative' },
    { code: 'INTJ', description: 'The Architect - Strategic and visionary' },
    { code: 'ISTP', description: 'The Virtuoso - Inventive and practical' },
    { code: 'ISFP', description: 'The Adventurer - Creative and expressive' },
    { code: 'INFP', description: 'The Mediator - Creative and selfless' },
    { code: 'INTP', description: 'The Thinker - Analytical and intellectual' },
    { code: 'ESTP', description: 'The Entrepreneur - Bold and energetic' },
    { code: 'ESFP', description: 'The Entertainer - Enthusiastic and friendly' },
    { code: 'ENFP', description: 'The Campaigner - Creative and enthusiastic' },
    { code: 'ENFJ', description: 'The Protagonist - Inspiring and perceptive' },
    { code: 'ENTJ', description: 'The Commander - Decisive and commanding' },
    { code: 'ESTJ', description: 'The Executive - Organized and pragmatic' },
    { code: 'ESFJ', description: 'The Consul - Personable and caring' },
    { code: 'ENTP', description: 'The Debater - Deceptive and clever' },
  ];

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox'
        ? prev[name] ? prev[name].filter(i => i !== value)
        : [...prev[name], value]
        : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // In production, actually call the API:
      // await API.registerUser(formData);
      console.log('Form submitted:', formData);
      alert('Profile saved successfully!');
    } catch (error) {
      console.error('Error saving profile:', error);
    }
  };

  return (
    <div className="page interest-form">
      <h1>Build Your Hobby Profile</h1>
      
      <form onSubmit={handleSubmit} className="interest-form-container">
        <div className="form-section">
          <h2>Personal Information</h2>
          
          <div className="form-group">
            <label htmlFor="name">Full Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              placeholder="Enter your name"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              placeholder="your@email.com"
              required
            />
          </div>
        </div>

        <div className="form-section">
          <h2>My Interests (Select all that apply)</h2>
          <div className="checkbox-grid">
            {interestOptions.map((interest) => (
              <div key={interest} className="checkbox-item">
                <input
                  type="checkbox"
                  name="interests"
                  value={interest}
                  checked={formData.interests.includes(interest)}
                  onChange={handleInputChange}
                />
                <label>{interest}</label>
              </div>
            ))}
          </div>
          
          <h2 style={{ marginTop: '2rem' }}>Your MBTI Personality Type</h2>
          <div className="checkbox-grid">
            {mbtiOptions.map((type) => (
              <div key={type.code} className="checkbox-item">
                <input
                  type="radio"
                  name="mbtiType"
                  value={type.code}
                  checked={formData.mbtiType === type.code}
                  onChange={handleInputChange}
                />
                <label>{`${type.code} - ${type.description}`}</label>
              </div>
            ))}
          </div>
        </div>

        <div className="form-section">
          <h2>Your Preferences</h2>
          
          <div className="form-group">
            <label>
              <input
                type="checkbox"
                checked={formData.preferences.indoor}
                onChange={(e) => setFormData(prev => ({
                  ...prev,
                  preferences: { ...prev.preferences, indoor: e.target.checked }
                }))}
              />
              Prefer indoor activities
            </label>
          </div>

          <div className="form-group">
            <label>
              <input
                type="checkbox"
                checked={formData.preferences.social}
                onChange={(e) => setFormData(prev => ({
                  ...prev,
                  preferences: { ...prev.preferences, social: e.target.checked }
                }))}
              />
              Prefer social/group activities
            </label>
          </div>
        </div>

        <div className="form-actions">
          <button type="submit" className="btn-primary">
            Generate My Hobby Plan
          </button>
        </div>
      </form>
    </div>
  );
}

export default InterestForm;