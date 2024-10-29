import axios from 'axios';

const API_BASE_URL = 'https://127.0.0.1:8080/api/calendarapi/';

export const fetchAvailability = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}availability/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching availability:', error);
    throw error;
  }
};

export const createInterview = async (interviewData) => {
  try {
    const response = await axios.post(
      `${API_BASE_URL}interviews/`,
      interviewData,
    );
    return response.data;
  } catch (error) {
    console.error('Error creating interview:', error);
    throw error;
  }
};

export const fetchEvents = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}events/`);
    return response.data.events;
  } catch (error) {
    console.error('Error fetching events:', error);
    throw error;
  }
};
