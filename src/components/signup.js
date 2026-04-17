import React, { useState } from 'react';
import '../styles/signup.css';

const SignUp = () => {
  const [confirmation, setConfirmation] = useState(null);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    username: '',
    location: '', 
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.password !== formData.confirmPassword) {
      setConfirmation("Passwords do not match.");
      return; 
    }

    const isUserAlreadySignedUp = await checkUserExists();

    if (isUserAlreadySignedUp) {
      setConfirmation('User with this email or username already exists.');
      return;
    } else {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/signup', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData),
        });

        if (response.ok) {
          console.log('User registered successfully');
          setConfirmation('Registration successful! You can now sign in.');
        } else {
          console.error('Error registering user:', await response.json());
          setConfirmation('Error registering user.');
        }
      } catch (error) {
        console.error('Error registering user:', error);
        setConfirmation('Error registering user. Please try again later.');
      }
    }
  };

  // Function to check if a user already exists based on email or username
  const checkUserExists = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/check_user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: formData.email,
          username: formData.username,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        return data.exists; 
      } else {
        console.error('Error checking user:', response.statusText);
        return false;
      }
    } catch (error) {
      console.error('Error checking user:', error);
      return false;
    }
  };

  // Options for the dropdown (all 50 US states)
  const usStates = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia',
    'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland',
    'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
    'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina',
    'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
  ];

  return (
    <div>
      <h2>Sign Up</h2>
      {confirmation && <p className='PopUp'>{confirmation}</p>}
      <form onSubmit={handleSubmit}>
        <label>
          Email:
          <br />
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </label>
        <br />
        <label>
          Password:
          <br />
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </label>
        <br />
        <label>
          Confirm Password:
          <br />
          <input
            type="password"
            name="confirmPassword"
            value={formData.confirmPassword}
            onChange={handleChange}
            required
          />
        </label>
        <br />
        <label>
          Username:
          <br />
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </label>
        <br />
        <label>
          Location:
          <br />
          <select
            name="location"
            value={formData.location}
            onChange={handleChange}
            required
          >
            <option value="" disabled>Select your state</option>
            {usStates.map((state, index) => (
              <option key={index} value={state}>{state}</option>
            ))}
          </select>
        </label>
        <br />
        <button type="submit">SIGN UP</button>
      </form>
    </div>
  );
};

export default SignUp;
