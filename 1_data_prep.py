import pandas as pd

def load_and_clean_data(file_path):
    print("Veri seti yükleniyor...")
    # CSV dosyasını oku
    df = pd.read_csv(file_path)
    
    # Bu veri setindeki yorumlar 'Review Text', yıldız puanları ise 'Rating' sütununda tutuluyor.
    # Adım 1: İçinde yorum metni bulunmayan (NaN/Boş) satırları ayıkla
    df = df.dropna(subset=['Review Text'])
    
    # Adım 2: İşlem kolaylığı için sütun isimlerini standartlaştır
    df = df.rename(columns={'Review Text': 'text', 'Rating': 'rating', 'Department Name': 'category'})
    
    # Sadece ihtiyacımız olan sütunları tut
    df = df[['text', 'rating', 'category']]
    
    # Adım 3: Embedding işlemi (vektör çevirimi) bilgisayarı yorabileceği için,
    # prototip (PoC) aşamasında sistemi test etmek amacıyla şimdilik rastgele 1000 yorumu alıyoruz.
    df = df.sample(n=1000, random_state=42).reset_index(drop=True)
    
    print(f"\nTemizlenmiş ve analize hazır yorum sayısı: {len(df)}")
    print("\n--- İlk 3 Yorum Örneği ---")
    for i in range(3):
        print(f"Kategori: {df['category'][i]} | Puan: {df['rating'][i]}")
        print(f"Yorum: {df['text'][i][:150]}...\n")
        
    return df

if __name__ == "__main__":
    # Kodu doğrudan çalıştırdığımızda bu blok tetiklenir
    temiz_veri = load_and_clean_data('data/reviews.csv')