# 1. Hafif bir Python tabanı seçiyoruz (Debian tabanlı slim versiyon)
FROM python:3.10-slim

# 2. Çalışma dizinini belirliyoruz
WORKDIR /app

# 3. İşletim sistemi seviyesindeki bağımlılıkları kuruyoruz (HDBSCAN ve ChromaDB derlemeleri için C++ derleyicisi gerekebilir)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Önce sadece requirements.txt'yi kopyalıyoruz (Docker'ın cache mekanizmasından faydalanmak için)
COPY requirements.txt .

# 5. Python bağımlılıklarını kuruyoruz
RUN pip install --no-cache-dir -r requirements.txt

# 6. Kodları ve önceden oluşturduğumuz vektör veritabanını (chroma_db) kopyalıyoruz
COPY . .

# 7. FastAPI'nin çalışacağı portu dışa açıyoruz
EXPOSE 8000

# 8. Konteyner ayağa kalktığında çalıştırılacak komut
CMD ["uvicorn", "5_fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]