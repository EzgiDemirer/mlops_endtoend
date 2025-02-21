# Python 3.10 tabanlı imajı kullan
FROM python:3.10

# Çalışma dizinini oluştur
WORKDIR /code

# Bağımlılıkları önce kopyala (cache optimizasyonu için)
COPY requirements.txt .

# Bağımlılıkları yükle
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Kalan tüm dosyaları kopyala
COPY . .

# Uygulamanın çalışacağı portu aç
EXPOSE 8080

# Uvicorn ile FastAPI uygulamasını başlat
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
