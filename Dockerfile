# Base image olarak Python kullan
FROM python:3.10

# Çalışma dizinini ayarla
WORKDIR /app

# Bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ana uygulama dosyasını kopyala
COPY . .

# FastAPI uygulamasını çalıştır
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
