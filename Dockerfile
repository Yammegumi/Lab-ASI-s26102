# Użycie lekkiego obrazu Pythona
FROM python:3.9-slim

# Ustawienie katalogu roboczego
WORKDIR /app

# Skopiowanie pliku requirements.txt i instalacja zależności
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Skopiowanie pozostałych plików aplikacji
COPY app.py .
COPY model.joblib .

# Wystawienie portu 5000
EXPOSE 5000

# Uruchomienie aplikacji
CMD ["python", "app.py"]
