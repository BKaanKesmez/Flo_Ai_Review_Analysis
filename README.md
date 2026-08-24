# 🛒 Akıllı Müşteri Yorum Analizi ve Semantik Arama Motoru (RAG Mimarisi)

Bu proje, e-ticaret platformlarındaki binlerce müşteri yorumunu geleneksel anahtar kelime (keyword) eşleştirmesi ötesine taşıyarak **anlamsal (semantik) bütünlükle** analiz eden, yapay zeka destekli bir tam yığın (full-stack) web uygulamasıdır. Sistem, **RAG (Retrieval-Augmented Generation)** mimarisinin temel yapı taşlarını kullanarak tasarlanmıştır.

Klasik arama motorları yazım hatalarında veya eş anlamlı kelimelerde başarısız olurken; bu mimari, Doğal Dil İşleme (NLP) modelleri ile metinleri matematiksel vektörlere dönüştürerek "kelimelerin anlamlarına ve bağlamlarına" göre arama yapar.

---

## 🚀 Mimarinin Temel Özellikleri

*   **Semantik Arama (Semantic Search):** Cümleler Sentence-Transformers modeli ile çok boyutlu uzayda vektörlere dönüştürülür. Örneğin "awful bottoms" araması, içinde doğrudan bu kelimeler geçmese bile "rahatsız edici, ince ve kötü kumaşlı pantolon" yorumlarını bulur.
*   **Hibrit Filtreleme (Hybrid Search):** Yapay zekanın "anlam" bulma gücü, geleneksel veritabanlarının "kesin filtreleme" (Metadata Filtering) mantığıyla birleştirilmiştir. Kullanıcı arayüzündeki tek bir parametre ile sorgular vektörel olarak taranırken, eşzamanlı olarak `rating <= 3` (sadece şikayetler) şartından geçirilir.
*   **Mobil Öncelikli (Mobile-First) Responsive Arayüz:** Frontend katmanı Tailwind CSS ile tasarlanmış olup, telefon, tablet ve masaüstü ekranlarda grid yapılarını dinamik olarak optimize eder.
*   **Kesintisiz Dağıtım (CI/CD):** GitHub Actions ve Vercel entegrasyonu sayesinde, ana dala (main branch) yapılan her kod gönderimi sıfır kesintiyle (zero-downtime) canlıya alınır.

---

## 🏗️ Kullanılan Teknolojiler ve Tech Stack

Proje mikroservis prensiplerine uygun olarak iki ana modülde geliştirilmiştir:

### 1. Backend & Yapay Zeka (AI API Katmanı)
*   **Framework:** `FastAPI` (Asenkron, yüksek performanslı ve Swagger entegreli)
*   **NLP Modeli:** `sentence-transformers/all-MiniLM-L6-v2` (Hızlı çıkarım süresi ve düşük bellek tüketimi için optimize edilmiş embedding modeli)
*   **Vektör Veritabanı:** `ChromaDB` (Müşteri yorumlarını, yıldız puanlarını ve kategori metadatalarını yüksek boyutlu vektör uzayında tutan yerel veritabanı)
*   **Altyapı (DevOps):** `Docker` (Uygulamanın izole edilmesi) & `Hugging Face Spaces` (API'nin bulutta barındırılması)

### 2. Frontend (Kullanıcı Arayüzü Katmanı)
*   **Framework:** `React.js` (Bileşen bazlı mimari)
*   **Stil/Tasarım:** `Tailwind CSS` (Utility-first, responsive tasarım)
*   **HTTP İstemcisi:** `Axios` (Backend ile RESTful iletişim)
*   **Hosting:** `Vercel` (Otomatik derleme ve global CDN dağıtımı)

---

## 📂 Proje Klasör Yapısı

Sistem; veri hazırlama, analiz, veritabanı inşası ve sunucu yayınlaması olmak üzere geniş bir Ar-Ge ve modüler script yelpazesinden oluşmaktadır:
```text
📦 flo_rag_project
 ┣ 📂 .github/               # CI/CD otomasyon (GitHub Actions) iş akışları
 ┣ 📂 chroma_db/             # Vektörleştirilmiş müşteri yorumları ve metadataları (Veritabanı)
 ┣ 📂 data/
 ┃ ┗ 📜 reviews.csv          # Ham e-ticaret müşteri yorumları veri seti
 ┣ 📂 flo-frontend/          # React.js (Vite) ile geliştirilmiş kullanıcı arayüzü
 ┃ ┣ 📂 src/
 ┃ ┃ ┣ 📂 assets/            # Statik görseller ve ikonlar
 ┃ ┃ ┣ 📜 api.js             # FastAPI sunucusuna Axios ile istek atan ağ servisi
 ┃ ┃ ┣ 📜 App.jsx            # Ana arayüz, RAG arama çubuğu ve State yönetimleri
 ┃ ┃ ┣ 📜 index.css          # Tailwind CSS yapılandırmaları
 ┃ ┃ ┗ 📜 main.jsx           # Uygulama başlangıç noktası
 ┃ ┣ 📜 package.json         # Frontend bağımlılıkları ve scriptleri
 ┃ ┣ 📜 tailwind.config.js   # Tailwind CSS stil ayarları
 ┃ ┗ 📜 vite.config.js       # Vite yapılandırma dosyası
 ┣ 📂 venv/                  # Python sanal ortamı (Virtual Environment)
 ┣ 📜 .dockerignore          # Docker imajından dışlanacak dosya kuralları
 ┣ 📜 .gitignore             # Git takibine alınmayacak dosya ve klasörler
 ┣ 📜 1_data_prep.py         # Ham e-ticaret verisini temizleme ve ön işleme betiği
 ┣ 📜 2_embedding_db.py      # Temiz veriyi vektöre çevirip ChromaDB'ye yazma betiği
 ┣ 📜 3_rag_retrieval.py     # RAG mimarisi için prototip arama (retrieval) test betiği
 ┣ 📜 4_clustering.py        # Yorumları semantik olarak kümeleme analiz betiği
 ┣ 📜 5_fastapi_app.py       # API Endpoint'lerini barındıran ana backend sunucusu
 ┣ 📜 6_streamlit_app.py     # Alternatif veri görselleştirme ve test arayüzü
 ┣ 📜 docker-compose.yml     # Çoklu konteyner orkestrasyonu yapılandırması
 ┣ 📜 Dockerfile             # Hugging Face deployment için konteyner yapılandırması
 ┗ 📜 README.md              # Proje dokümantasyonu
 ```


 ## 📡 API Dokümantasyonu (Endpoint'ler)

Backend uygulaması çalıştırıldığında `/docs` dizininde otomatik olarak Swagger UI dokümantasyonu oluşur.

### GET `/search`
Verilen anahtar kelimenin anlamsal karşılığını veritabanında arar ve metadataları filtreler.

| Parametre | Tip | Açıklama | Varsayılan |
| :--- | :--- | :--- | :--- |
| `q` | `string` | Kullanıcının aradığı metin veya şikayet cümlesi | **Zorunlu** |
| `only_complaints` | `boolean` | `true` ise sadece rating'i 3 ve altında olan yorumları getirir. | `false` |

**Örnek İstek (Sadece şikayetler):**
`GET https://<HUGGING_FACE_URL>/search?q=awfull%20bottoms&only_complaints=true`

---

## ⚙️ Kurulum ve Yerel Geliştirme (Local Development)

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

### 1. Backend Kurulumu
1. Repoyu klonlayın ve backend dizinine gidin.
2. Python sanal ortamı oluşturup aktif edin (`python -m venv venv` ve `source venv/bin/activate`).
3. Gerekli kütüphaneleri yükleyin: `pip install -r requirements.txt`
4. FastAPI sunucusunu başlatın:
   ```bash
   uvicorn 5_fastapi_app:app --host 0.0.0.0 --port 8000 --reload


## 💻 Frontend Kurulumu ve Çalıştırma

Kullanıcı arayüzünü yerel ortamınızda ayağa kaldırmak ve FastAPI backend'i ile haberleştirmek için şu adımları izleyin:

1. **Frontend Dizinine Geçiş:**
   Terminal üzerinden projenin içindeki React klasörüne gidin:
   ```bash
   cd flo-frontend```

2. **Bağımlılıkların Yüklenmesi:**
    Projede kullanılan npm paketlerini (Tailwind CSS, Axios vb.) yükleyin: 
    ```npm install```

3. **API Bağlantı Ayarı (src/api.js):**

    Yerel testler için src/api.js dosyasındaki baseURL değerinin http://localhost:8000 (veya backend'i çalıştırdığınız yerel port) olduğundan emin olun.

    Canlı ortam testleri için bu adresin Hugging Face Docker URL'si (https://<username>-flo-ai-backend.hf.space) olarak ayarlanması gerekir.

4. **Geliştirme Sunucusunun Başlatılması:**
    Vite ile yerel sunucuyu ayağa kaldırın:
    ```npm run dev ```

    (Tarayıcınızda http://localhost:5173 (veya terminalde belirtilen adres) üzerinden arayüze erişebilirsiniz.)


## ☁️ Bulut Mimarisi ve Deployment Stratejisi

Proje, üretim ortamında (Production) yüksek erişilebilirlik ve düşük maliyet (FinOps) prensipleri gözetilerek modern bulut servislerine dağıtılmıştır:

1. **API Katmanı (Hugging Face Docker Spaces):**

    Ağır yapay zeka modelleri (sentence-transformers) ve ChromaDB vektör veritabanı içeren backend uygulaması, donanımsal tutarlılık ve bağımlılık izolasyonu için Dockerfile ile paketlenmiştir.

    Hugging Face Docker altyapısı üzerinde EXPOSE 7860 portu üzerinden dış dünyaya güvenli HTTPS protokolüyle açılmıştır.

    Maliyet Optimizasyonu (FinOps): Sistem, gereksiz kaynak tüketimini önlemek amacıyla 1 saatlik inaktiflik sonrasında otomatik olarak uyku moduna (Auto-sleep) geçecek şekilde yapılandırılmıştır.

2. **Arayüz Katmanı (Vercel Global CDN):**

    React tabanlı kullanıcı arayüzü, GitHub reosu ile entegre edilmiştir.

    Ana dala (main) yapılan her başarılı git push komutu sonrasında Vercel tarafından otomatik olarak derlenir (CI/CD) ve sıfır kesintiyle (zero-downtime) dünyanın dört bir yanındaki uç sunuculara (CDN) dağıtılır.


**Geliştirici : Buğra Kaan Kesmez**