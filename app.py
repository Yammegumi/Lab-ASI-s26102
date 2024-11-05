import pandas as pd
from flask import Flask, request, jsonify
from joblib import load
import logging
import warnings

# Ignorowanie ostrzeżeń
warnings.filterwarnings('ignore')

# Konfiguracja loggera
logging.basicConfig(
    filename='prediction_app.log',
    level=logging.DEBUG,
    format='%(levelname)s:%(asctime)s: %(message)s',
    filemode='w'
)

# Inicjalizacja aplikacji Flask
app = Flask(__name__)

# Wczytanie modelu
model = load('model.joblib')

# Definicja listy oczekiwanych kolumn
expected_columns = ['unemp', 'wage', 'distance', 'tuition', 'education',
                    'gender', 'ethnicity', 'fcollege', 'mcollege', 'home', 'urban', 'income', 'region']

# Definicja endpointu
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Pobranie danych z requestu
        data = request.get_json()
        logging.info(f'Pobrano dane: {data}')

        # Konwersja danych do DataFrame
        input_data = pd.DataFrame([data])

        # Upewnienie się, że kolumny są w odpowiedniej kolejności
        input_data = input_data[expected_columns]

        # Przewidywanie
        prediction = model.predict(input_data)
        logging.info(f'Przewidywanie: {prediction}')

        # Zwrócenie wyniku
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        logging.error(f'Błąd podczas przewidywania: {e}')
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
