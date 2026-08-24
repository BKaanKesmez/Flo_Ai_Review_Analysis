import axios from 'axios';

const api = axios.create({
    baseURL: 'https://laxryy-flo-ai-backend.hf.space/', // FastAPI Backend Adresimiz
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