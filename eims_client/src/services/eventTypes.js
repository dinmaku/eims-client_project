import axios from 'axios';

const API_URL = 'http://localhost:5000'; // Update this with your backend URL

export const fetchEventTypes = async () => {
  try {
    const response = await axios.get(`${API_URL}/event-types`);
    return response.data;
  } catch (error) {
    console.error('Error fetching event types:', error);
    throw error;
  }
};
