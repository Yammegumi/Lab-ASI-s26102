import requests

# URL endpointu API
url = 'http://localhost:5000/predict'

# Dane wejściowe
data = {
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
}

try:
    # Wysyłanie żądania POST z danymi JSON
    response = requests.post(url, json=data)
    response.raise_for_status()  # Sprawdzenie, czy nie wystąpił błąd HTTP

    # Wyświetlenie odpowiedzi
    print("Odpowiedź z serwera:")
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"Błąd podczas komunikacji z API: {e}")
