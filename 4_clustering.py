import chromadb
import hdbscan
import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize

def discover_review_clusters():
    print("1. Veritabanına bağlanılıyor ve vektörler çekiliyor...")
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_collection(name="flo_reviews")
    
    # Tüm verileri veritabanından getir
    results = collection.get(include=['embeddings', 'documents', 'metadatas'])
    
    embeddings = np.array(results['embeddings'])
    documents = results['documents']
    
    print(f"Toplam {len(embeddings)} adet yorum vektörü analiz ediliyor...")

    # Vektörleri normalize edelim (Kosinüs benzerliğinin doğru çalışması için önemli bir matematiksel adımdır)
    normalized_embeddings = normalize(embeddings)

    print("2. HDBSCAN algoritması çalıştırılıyor (Bu işlem verinin boyutuna göre birkaç saniye sürebilir)...")
    # min_cluster_size=5 : Bir sorunun kronik (küme) sayılması için en az 5 benzer yorum olmalı
    # metric='euclidean' : Normalize edilmiş vektörlerde Öklid uzaklığı, Kosinüs uzaklığı ile aynı mantıkta çalışır
    clusterer = hdbscan.HDBSCAN(min_cluster_size=5, metric='euclidean')
    labels = clusterer.fit_predict(normalized_embeddings)

    # 3. Sonuçları bir DataFrame'de toplayıp analiz edelim
    df_results = pd.DataFrame({
        'Yorum': documents,
        'Kume_ID': labels
    })

    # Küme ID'si -1 olanlar "Gürültü" (hiçbir gruba girmeyen benzersiz yorumlar) demektir[cite: 1].
    toplam_kume_sayisi = len(set(labels)) - (1 if -1 in labels else 0)
    
    print(f"\n--- KÜMELEME SONUÇLARI ---")
    print(f"Otomatik tespit edilen farklı şikayet/yorum grubu sayısı: {toplam_kume_sayisi}")
    print(f"Hiçbir gruba uymayan (Gürültü) yorum sayısı: {list(labels).count(-1)}")
    
    print("\n--- EN BÜYÜK 3 KRONİK YORUM GRUBU ---")
    # -1 (gürültü) hariç kümeleri boyutlarına göre sırala
    clusters = df_results[df_results['Kume_ID'] != -1]['Kume_ID'].value_counts()
    
    for kume_id, count in clusters.head(3).items():
        print(f"\n>> Küme {kume_id} (Bu grupta {count} benzer yorum var):")
        # Bu kümeye ait rastgele 3 yorumu göster
        ornek_yorumlar = df_results[df_results['Kume_ID'] == kume_id]['Yorum'].head(3).tolist()
        for idx, yorum in enumerate(ornek_yorumlar):
            # Uzun yorumları keserek gösterelim
            print(f"  {idx+1}. {yorum[:120]}...")

if __name__ == "__main__":
    discover_review_clusters()