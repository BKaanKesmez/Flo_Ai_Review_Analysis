import chromadb
from sentence_transformers import SentenceTransformer

def search_reviews(query, top_k=3):
    print(f"\nSoru: '{query}'")
    print("Veritabanında anlamsal arama yapılıyor...\n")
    
    # 1. ChromaDB'ye bağlan (Önceki adımda oluşturduğumuz veritabanı)
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_collection(name="flo_reviews")
    
    # 2. Aynı modeli kullanarak soruyu vektöre çevir (Embedding)
    # Soru ve yorumların aynı uzayda eşleşmesi için modelin birebir aynı olması şarttır.
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode([query]).tolist()
    
    # 3. Vektör veritabanında en yakın sonuçları getir (Top-k retrieval)[cite: 1]
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )
    
    # 4. Sonuçları formatla ve ekrana bas
    for i in range(top_k):
        review_text = results['documents'][0][i]
        metadata = results['metadatas'][0][i]
        distance = results['distances'][0][i] # Kosinüs uzaklığı (Mesafe ne kadar küçükse anlam o kadar benzerdir)[cite: 1]
        
        print(f"--- Sonuç {i+1} ---")
        print(f"Kategori: {metadata['category']} | Puan: {metadata['rating']} Yıldız")
        print(f"Yorum: {review_text}")
        print(f"Uzaklık Skoru: {distance:.4f}\n")

if __name__ == "__main__":
    # Test Senaryosu 1: Pozitif bir arama (Rahat ayakkabılar)
    test_query_1 = "I am looking for comfortable shoes for running and walking." 
    search_reviews(test_query_1)
    
    print("=========================================")
    
    # Test Senaryosu 2: Negatif bir şikayet araması (Kötü malzeme)
    test_query_2 = "The material is very poor quality and it tore quickly."
    search_reviews(test_query_2)