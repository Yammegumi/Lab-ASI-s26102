# CollegeDistance Prediction API

Aplikacja umożliwia przewidywanie wartości `score` na podstawie danych z zestawu `CollegeDistance`. API zostało zbudowane przy użyciu Flask i jest konteneryzowane za pomocą Dockera.

## Spis treści

- [Wymagania wstępne](#wymagania-wstępne)
- [Rozpoczęcie pracy](#rozpoczęcie-pracy)
  - [Klonowanie repozytorium](#klonowanie-repozytorium)
  - [Trenowanie modelu](#trenowanie-modelu)
  - [Uruchamianie aplikacji lokalnie](#uruchamianie-aplikacji-lokalnie)
  - [Uruchamianie aplikacji z wykorzystaniem Dockera](#uruchamianie-aplikacji-z-wykorzystaniem-dockera)
- [Korzystanie z API](#korzystanie-z-api)
  - [Przykładowe zapytanie](#przykładowe-zapytanie)
- [Obraz na Docker Hub](#obraz-na-docker-hub)
  - [Pobieranie obrazu](#pobieranie-obrazu)
  - [Uruchamianie kontenera](#uruchamianie-kontenera)

## Wymagania wstępne

- Python 3.7 lub nowszy
- Docker zainstalowany na Twoim systemie

## Rozpoczęcie pracy

### Klonowanie repozytorium

```bash
git clone https://github.com/Yammegumi/Lab-ASI-s26102.git
```

## Trenowanie modelu
Przed uruchomieniem aplikacji musisz wytrenować model:
```bash
python train_model.py
```
## Uruchamianie aplikacji lokalnie
Zainstaluj wymagane pakiety:
```bash
pip install -r requirements.txt
```
Uruchom aplikację Flask:
```bash
python app.py
```

Aplikacja będzie dostępna pod adresem http://localhost:5000.

## Uruchamianie aplikacji z wykorzystaniem Dockera
Zbuduj obraz Dockera:
```bash
docker build -t yammegumi/collegedistance-prediction .
```
Uruchom kontener:
```bash
docker run -p 5000:5000 yammegumi/collegedistance-prediction
```

Aplikacja będzie dostępna pod adresem http://localhost:5000.

## Korzystanie z API

Wyślij żądanie POST na endpoint **/predict** z danymi w formacie JSON.

### Przykładowe zapytanie

```bash
curl -X POST http://localhost:5000/predict \
    -H "Content-Type: application/json" \
    -d '{
        "unemp": 6.0,
        "wage": 10.0,
        "distance": 5.0,
        "tuition": 5000.0,
        "education": 12.0,
        "gender": "female",
        "ethnicity": "white",
        "fcollege": "no",
        "mcollege": "no",
        "home": "yes",
        "urban": "no",
        "income": "high",
        "region": "south"
    }'
```

Alternatywnie użyj skryptu client.py

## Obraz na Docker Hub
Obraz Dockera jest dostępny na Docker Hub: yammegumi/collegedistance-prediction

### Pobieranie obrazu
```bash
docker pull yammegumi/collegedistance-prediction
```
### Uruchamianie kontenera
```bash
docker run -p 5000:5000 yammegumi/collegedistance-prediction
```
Aplikacja będzie dostępna pod adresem http://localhost:5000.