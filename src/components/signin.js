import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/signup.css';

const SignIn = () => {
  const [confirmation, setConfirmation] = useState(null);
  const [formData, setFormData] = useState({
    emailOrUsername: '', 
    password: '',
  });
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Call the signin API
      const response = await fetch('http://127.0.0.1:5000/api/signin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json(); 

      if (response.ok) {
        console.log('User signed in successfully');
        localStorage.setItem('token', data.access_token); // Store the JWT token
        setConfirmation('Signed in successfully'); 
        navigate('/');
      } else if (response.status === 401) {
        console.error('Incorrect username/email or password');
        setConfirmation('Incorrect username/email or password');
      } else {
        console.error('Error signing in:', await response.json());
        setConfirmation('Error signing in');
      }
    } catch (error) {
      console.error('Error signing in:', error);
      setConfirmation('Error signing in');
    }
  };

  return (
    <div>
      <h2>Sign In</h2>
      {confirmation && <p className='PopUp'>{confirmation}</p>}
      <form onSubmit={handleSubmit}>
        <label>
          Email or UserName:
          <br />
          <input
            type="text" 
            name="emailOrUsername"
            value={formData.emailOrUsername}
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
        <br/>
        <button type="submit">SIGN IN</button>
        <br />
      </form>
    </div>
  );
};

export default SignIn;
