import streamlit as st
import requests
import pandas as pd
import chromadb
import hdbscan
import numpy as np
from sklearn.preprocessing import normalize

# 1. Sayfa Ayarları ve Başlık
st.set_page_config(page_title="Flo Yorum Analizi", page_icon="👟", layout="wide")
st.title("👟 Flo Akıllı Müşteri Yorumları Analiz Paneli")
st.markdown("Bu panel, yapay zeka destekli anlamsal arama (RAG) ve HDBSCAN algoritması ile otomatik şikayet kümeleme işlevlerini içerir.")

# 2. İki Ayrı Sekme (Tab) Oluşturma
tab1, tab2 = st.tabs(["💬 RAG Asistanı (Anlamsal Arama)", "📊 Şikayet Kümeleme (Clustering)"])

# ----------------- SEKME 1: RAG ASİSTANI -----------------
with tab1:
    st.header("Müşteri Yorumlarında Akıllı Arama")
    st.write("Klasik anahtar kelime araması yerine, anlamsal (semantik) olarak benzer yorumları bulur.")
    
    query = st.text_input("Araştırmak istediğiniz şikayeti veya konuyu girin (Örn: shoes are very uncomfortable, bad material)")
    
    if st.button("Yorumları Bul (API'ye İstek At)"):
        if query:
            with st.spinner("Docker üzerindeki FastAPI'den sonuçlar getiriliyor..."):
                try:
                    # Docker'da 8000 portunda çalışan API'mize istek atıyoruz
                    response = requests.get(f"http://127.0.0.1:8000/search?q={query}&top_k=3")
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.success(f"Bulunan Sonuç Sayısı: {data['bulunan_sonuc_sayisi']}")
                        
                        # Sonuçları genişletilebilir (expander) kartlar halinde göster
                        for idx, res in enumerate(data['sonuclar']):
                            with st.expander(f"Sonuç {idx+1} - Kategori: {res['kategori']} | Puan: {res['puan']}⭐"):
                                st.write(f"**Yorum:** {res['yorum']}")
                                st.caption(f"Benzerlik (Kosinüs Uzaklığı) Skoru: {res['uzaklik_skoru']}")
                    else:
                        st.error("API'den hata döndü.")
                except Exception as e:
                    st.error(f"API'ye bağlanılamadı. Docker konteynerinin çalıştığından emin olun. Hata: {e}")
        else:
            st.warning("Lütfen bir arama metni girin.")

# ----------------- SEKME 2: KÜMELEME (CLUSTERING) -----------------
with tab2:
    st.header("Otomatik Şikayet Kümeleme (HDBSCAN)")
    st.write("Veritabanındaki binlerce yorum anlamsal olarak analiz edilecek ve aynı sorunu yaşayan müşteriler otomatik olarak gruplanacaktır.")
    
    if st.button("Kümeleme Analizini Başlat"):
        with st.spinner("HDBSCAN algoritması çalışıyor (Bu işlem birkaç saniye sürebilir)..."):
            try:
                # Vektör veritabanından verileri çekiyoruz
                chroma_client = chromadb.PersistentClient(path="./chroma_db")
                collection = chroma_client.get_collection(name="flo_reviews")
                results = collection.get(include=['embeddings', 'documents'])
                
                embeddings = np.array(results['embeddings'])
                documents = results['documents']
                
                # Kosinüs benzerliği için vektörleri normalize ediyoruz
                normalized_embeddings = normalize(embeddings)
                
                # HDBSCAN modelini çalıştır
                clusterer = hdbscan.HDBSCAN(min_cluster_size=5, metric='euclidean')
                labels = clusterer.fit_predict(normalized_embeddings)
                
                df_results = pd.DataFrame({'Yorum': documents, 'Kume_ID': labels})
                
                # İstatistikleri hesapla
                toplam_kume_sayisi = len(set(labels)) - (1 if -1 in labels else 0)
                gurultu_sayisi = list(labels).count(-1)
                
                # Metrikleri yan yana göster
                col1, col2 = st.columns(2)
                col1.metric("Tespit Edilen Kronik Şikayet Grubu", toplam_kume_sayisi)
                col2.metric("Gürültü (Hiçbir gruba uymayan yorumlar)", gurultu_sayisi)
                
                st.markdown("---")
                st.subheader("En Büyük Şikayet Kümeleri (Kronik Sorunlar)")
                
                clusters = df_results[df_results['Kume_ID'] != -1]['Kume_ID'].value_counts()
                
                for kume_id, count in clusters.head(3).items():
                    st.markdown(f"### 🛑 Küme {kume_id} (Grup Büyüklüğü: {count} Yorum)")
                    ornek_yorumlar = df_results[df_results['Kume_ID'] == kume_id]['Yorum'].head(3).tolist()
                    for i, yorum in enumerate(ornek_yorumlar):
                        st.info(f"{i+1}. {yorum}")
                        
            except Exception as e:
                st.error(f"Kümeleme sırasında bir hata oluştu: {e}")