import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';

test('creates a new user account', async () => {
    // Mock server response
    global.fetch = jest.fn(() =>
      Promise.resolve({ status: 201 }) // Status 201 for Created
    );
  
    const userData = { username: 'newuser', password: 'password123' };
    const response = await createUser(userData);
  
    expect(response.status).toBe(201);
});

test('logs in a user', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        status: 200,
        json: () => Promise.resolve({ token: 'some_auth_token' }), // Example token response
      })
    );
  
    const credentials = { username: 'user', password: 'password' };
    const response = await loginUser(credentials);
  
    expect(response.status).toBe(200);
    await response.json().then(data => {
      expect(data).toHaveProperty('token');
    });
});