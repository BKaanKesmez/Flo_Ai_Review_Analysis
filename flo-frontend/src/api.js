import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000', // FastAPI Backend Adresimiz
});

export const searchReviews = async (query) => {
    try {
        const response = await api.get(`/search?q=${query}&top_k=5`);
        return response.data.sonuclar;
    } catch (error) {
        console.error("Backend bağlantı hatası:", error);
        return [];
    }
};