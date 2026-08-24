from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import chromadb
from sentence_transformers import SentenceTransformer
import uvicorn

# 1. API Uygulamasını Başlat
app = FastAPI(
    title="Flo Müşteri Yorumları Analiz API",
    description="RAG ve Kümeleme tabanlı akıllı e-ticaret analiz servisi",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Tüm domainlere izin ver (Geliştirme ortamı için)
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


print("Yapay Zeka Modeli ve Veritabanı Yükleniyor... (Lütfen bekleyin)")
# Modeli ve DB'yi global olarak yüklüyoruz ki her istekte baştan yüklenip sistemi yavaşlatmasın
model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="flo_reviews")
print("Sistem API istekleri için hazır!")




# 2. Kök Dizin (Ana Sayfa)
@app.get("/")
def read_root():
    return {"mesaj": "Flo Akıllı Analiz Mikroservisine Hoş Geldiniz. Dökümantasyon için /docs adresine gidin."}

# 3. Anlamsal Arama (Semantic Search / RAG Retrieval) Uç Noktası
@app.get("/search")
def search_reviews(q: str = Query(..., description="Aranacak şikayet veya yorum"), top_k: int = 3):
    # Soruyu vektöre çevir
    query_embedding = model.encode([q]).tolist()
    
    # Veritabanında ara
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )
    
    # API'nin döndüreceği temiz JSON formatı
    response_data = []
    for i in range(top_k):
        response_data.append({
            "kategori": results['metadatas'][0][i]['category'],
            "puan": results['metadatas'][0][i]['rating'],
            "yorum": results['documents'][0][i],
            "uzaklik_skoru": round(results['distances'][0][i], 4)
        })
        
    return {
        "sorgu": q,
        "bulunan_sonuc_sayisi": top_k,
        "sonuclar": response_data
    }

if __name__ == "__main__":
    # Uygulamayı lokal sunucuda ayağa kaldır
    uvicorn.run("5_fastapi_app:app", host="0.0.0.0", port=8000, reload=True)