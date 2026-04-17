import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import PlayerStats from './PlayerStats';
import '@testing-library/jest-dom';

// Mock Fetch API
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({
      items: [{ Player: 'Brandon Aubrey', FGM: 36, Att: 38, FG_percent: 94.7, Lng: 60, Fg_Blk: 1 }], 
      pages: 3,
    }),
  })
);

beforeEach(() => {
  fetch.mockClear();
});

test('displays stats after fetching', async () => {
  render(<PlayerStats />);

  // Wait for the fetch to complete and the component to update
  await waitFor(() => {
    expect(screen.getByText('Brandon Aubrey')).toBeInTheDocument();
    expect(screen.getByText('3')).toBeInTheDocument(); // Example: FGM stat
    // Test for other stats here
  });
});

test('pagination controls work correctly', async () => {
    render(<PlayerStats />);
  
    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument(); // Initial data load check
    });
  
    // Assuming you have buttons with test IDs for Previous and Next
    const nextButton = screen.getByTestId('next-page');
    const prevButton = screen.getByTestId('previous-page');
  
    // Simulate clicking the Next button
    userEvent.click(nextButton);
  
    await waitFor(() => {
      // Check if the fetch was called with the next page number
      expect(fetch).toHaveBeenCalledWith(expect.stringContaining('page=2'));
    });
  
    // Simulate clicking the Previous button
    userEvent.click(prevButton);
  
    await waitFor(() => {
      // Check if the fetch was called with the previous page number
      expect(fetch).toHaveBeenCalledWith(expect.stringContaining('page=1'));
    });
  });

