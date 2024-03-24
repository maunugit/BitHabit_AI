import axios from 'axios';

const api = axios.create({
    // baseURL: 'https://maunu.pythonanywhere.com/' // Flask API URL
    baseURL: 'http://127.0.0.1:5000'
    // baseUrl: 'http://localhost:5000/'
});

export const sendMessage = async (message) => {
    try {
        const response = await api.post('/message', { message }); // endpoint for the message that is sent
        return response.data;
    } catch (error) {
        console.error('Error sending message to API:', error);
        throw error;
    }
};
