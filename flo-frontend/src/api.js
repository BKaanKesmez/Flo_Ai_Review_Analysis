import axios from 'axios';

const api = axios.create({
    baseURL: 'https://laxryy-flo-ai-backend.hf.space/', // FastAPI Backend Adresimiz
});

export const searchReviews = async (query , onlyComplaints = false) => {
    try {
        const response = await api.get(`/search?q=${query}&only_complaints=${onlyComplaints}&top_k=5`);
        return response.data.sonuclar;
    } catch (error) {
        console.error("Backend bağlantı hatası:", error);
        return [];
    }
};