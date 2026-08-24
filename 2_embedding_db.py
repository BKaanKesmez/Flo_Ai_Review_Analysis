import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
import torch

def create_vector_db():
    print("1. ChromaDB Başlatılıyor...")
    # Veritabanını lokalde 'chroma_db' adında bir klasöre kaydedeceğiz[cite: 1]
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    
    # 'flo_reviews' adında bir koleksiyon (tablo) oluştur (varsa sıfırlıyoruz)
    collection_name = "flo_reviews"
    try:
        chroma_client.delete_collection(name=collection_name)
    except Exception:
        pass
    collection = chroma_client.create_collection(name=collection_name)

    print("2. Embedding Modeli Yükleniyor...")
    # Ekran kartının CUDA çekirdeklerini kullanarak işlemi hızlandırıyoruz
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Kullanılan donanım: {device.upper()}")
    
    # Hızlı ve e-ticaret metinleri için etkili bir İngilizce model seçiyoruz
    model = SentenceTransformer('all-MiniLM-L6-v2', device=device)

    print("3. Veri Hazırlanıyor...")
    df = pd.read_csv('data/reviews.csv')
    df = df.dropna(subset=['Review Text'])
    df = df.rename(columns={'Review Text': 'text', 'Rating': 'rating', 'Department Name': 'category'})
    df = df[['text', 'rating', 'category']]
    df = df.sample(n=1000, random_state=42).reset_index(drop=True)

    print("4. Chunking ve Vektörizasyon (Embedding) Başlıyor...")
    # 1 Yorum = 1 Chunk mantığı[cite: 1]
    documents = df['text'].tolist()
    
    # Metadata (Filtreleme için ek bilgiler)[cite: 1]
    metadatas = [{"rating": row['rating'], "category": str(row['category'])} for _, row in df.iterrows()]
    ids = [f"yorum_{i}" for i in range(len(df))]

    # Vektörleri oluştur (Embedding işlemi)[cite: 1]
    print(f"{len(documents)} adet yorum vektörlere dönüştürülüyor...")
    embeddings = model.encode(documents, show_progress_bar=True).tolist()

    print("5. Vektör Veritabanına Kaydediliyor...")
    collection.add(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    
    print("\nHarika! Tüm yorumlar vektörlere çevrilip ChromaDB'ye başarıyla kaydedildi.")
    print(f"Veritabanındaki toplam kayıt sayısı: {collection.count()}")

if __name__ == "__main__":
    create_vector_db()