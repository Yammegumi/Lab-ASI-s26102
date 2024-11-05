import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (mean_absolute_error, mean_squared_error,
                             r2_score, mean_absolute_percentage_error)
import logging
import warnings
from joblib import dump

# Ignorowanie ostrzeżeń
warnings.filterwarnings('ignore')

# Konfiguracja loggera
logging.basicConfig(
    filename='data_prediction.log',
    level=logging.DEBUG,
    format='%(levelname)s:%(asctime)s: %(message)s',
    filemode='w'
)

# Wczytanie danych
data = pd.read_csv('CollegeDistance.csv')

# Definicja zmiennych numerycznych i kategorycznych
numerical_features = ['unemp', 'wage', 'distance', 'tuition', 'education']
categorical_features = ['gender', 'ethnicity', 'fcollege', 'mcollege', 'home', 'urban', 'income', 'region']

# Definicja zmiennej docelowej
target_variable = 'score'

# Podział danych na cechy i target
X = data.drop(columns=[target_variable])
y = data[target_variable]

# Podział na zbiór treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Transformacje dla cech numerycznych
numeric_transformer = make_pipeline(
    KNNImputer(n_neighbors=5),
    MinMaxScaler()
)

# Transformacje dla cech kategorycznych
categorical_transformer = make_pipeline(
    SimpleImputer(strategy='most_frequent'),
    OneHotEncoder(handle_unknown='ignore')
)

# Połączenie transformacji
preprocessor = make_column_transformer(
    (numeric_transformer, numerical_features),
    (categorical_transformer, categorical_features)
)

# Utworzenie pełnego pipeline z modelem
model_pipeline = make_pipeline(
    preprocessor,
    RandomForestRegressor(random_state=42)
)

# Parametry do przeszukania
param_distributions = {
    'randomforestregressor__n_estimators': [100, 200, 300],
    'randomforestregressor__max_depth': [None, 10, 20],
    'randomforestregressor__min_samples_split': [2, 5],
    'randomforestregressor__min_samples_leaf': [1, 2],
    'randomforestregressor__bootstrap': [True, False]
}

# Inicjalizacja RandomizedSearchCV
random_search = RandomizedSearchCV(
    estimator=model_pipeline,
    param_distributions=param_distributions,
    n_iter=10,
    cv=5,
    scoring='neg_mean_squared_error',
    random_state=42,
    n_jobs=-1,
    verbose=1
)

# Trenowanie modelu z optymalizacją hiperparametrów
random_search.fit(X_train, y_train)

# Najlepsze parametry
best_params = random_search.best_params_
logging.info(f'Najlepsze parametry: {best_params}')

# Przewidywanie na zbiorze testowym
y_pred = random_search.predict(X_test)

# Obliczanie metryk
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)
mape = mean_absolute_percentage_error(y_test, y_pred)

# Logowanie wyników
logging.info(f'MSE na zbiorze testowym: {mse:.4f}')
logging.info(f'MAE na zbiorze testowym: {mae:.4f}')
logging.info(f'RMSE na zbiorze testowym: {rmse:.4f}')
logging.info(f'R^2 na zbiorze testowym: {r2:.4f}')
logging.info(f'MAPE na zbiorze testowym: {mape:.4f}')

# Wyświetlanie wyników
print('Wyniki na zbiorze testowym:')
print(f'MSE: {mse:.4f}')
print(f'MAE: {mae:.4f}')
print(f'RMSE: {rmse:.4f}')
print(f'R^2: {r2:.4f}')
print(f'MAPE: {mape:.4f}')

# Zapisanie wytrenowanego modelu do pliku
dump(random_search.best_estimator_, 'model.joblib')
