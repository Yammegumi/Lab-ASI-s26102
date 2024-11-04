import logging
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from google.oauth2 import service_account
from googleapiclient.discovery import build
import argparse


# Konfiguracja loggera
def setup_logger():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()])
    return logging.getLogger()


logger = setup_logger()

# Konfiguracja Google API
SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1EkhMgaBIaMRNNoJQEy09ZEiPUXrBZgZxXBZ39S8Qowo'
RANGE_NAME = 'Arkusz1!A1:Z'


# Autoryzacja Google Sheets
def authorize_google_service():
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('sheets', 'v4', credentials=credentials)


service = authorize_google_service()


# Odczyt danych z pliku CSV
def read_csv_data(file_path):
    logger.info("Wczytywanie danych z pliku CSV...")
    df = pd.read_csv(file_path).fillna("")  # Zakładamy przecinek jako separator
    logger.info("Dane zostały wczytane pomyślnie.")
    return df


# Odczyt danych z Google Sheets
def fetch_google_sheet_data():
    logger.info("Pobieranie danych z Google Sheets...")
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])
    if not values:
        logger.error("Brak danych w arkuszu.")
        return pd.DataFrame()
    return pd.DataFrame(values[1:], columns=values[0])


# Czyszczenie Google Sheets
def clear_google_sheet():
    logger.info("Czyszczenie arkusza Google Sheets...")
    service.spreadsheets().values().clear(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()


# Aktualizacja Google Sheets
def update_google_sheet(df):
    logger.info("Aktualizacja arkusza Google Sheets...")
    clear_google_sheet()
    body = {'values': [df.columns.tolist()] + df.values.tolist()}
    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
        valueInputOption='RAW', body=body).execute()
    logger.info("Aktualizacja zakończona.")


# Czyszczenie danych
def clean_data(df, missing_threshold=0.5):
    logger.info("Rozpoczynanie czyszczenia danych...")
    df = df.replace("", np.nan)
    threshold = int(len(df.columns) * (1 - missing_threshold))
    df_cleaned = df.dropna(thresh=threshold)

    empty_before = df.isnull().sum().sum()
    for col in df_cleaned.columns:
        if df_cleaned[col].dtype in [np.int64, np.float64]:
            df_cleaned[col].fillna(df_cleaned[col].median(), inplace=True)
        else:
            df_cleaned[col].fillna("Brak danych", inplace=True)

    empty_after = df_cleaned.isnull().sum().sum()
    logger.info("Czyszczenie danych zakończone.")
    return df_cleaned, empty_before, empty_after


# Standaryzacja danych
def standardize_data(df):
    logger.info("Standaryzacja danych...")
    df_standardized = df.copy()
    encoders = {}

    for col in df_standardized.select_dtypes(include='object').columns:
        le = LabelEncoder()
        df_standardized[col] = le.fit_transform(df_standardized[col])
        encoders[col] = le

    scaler = StandardScaler()
    df_standardized[df_standardized.columns] = scaler.fit_transform(df_standardized[df_standardized.columns])
    logger.info("Standaryzacja zakończona.")
    return df_standardized


# Główna funkcja
def main():
    parser = argparse.ArgumentParser(description="Opcje: --upload (upload danych do Google Sheets) --standardize (czyszczenie i standaryzacja danych)")
    parser.add_argument('--upload', type=str, help="Ścieżka do pliku CSV do wczytania i uploadu do Google Sheets")
    parser.add_argument('--standardize', action='store_true', help="Przeprowadzenie czyszczenia i standaryzacji danych")

    args = parser.parse_args()

    if args.upload:
        df = read_csv_data(args.upload)
        update_google_sheet(df)

    elif args.standardize:
        df = fetch_google_sheet_data()
        if df.empty:
            logger.error("Błąd przy odczycie danych z Google Sheets.")
            return

        rows_before = df.shape[0]
        df_cleaned, empty_before, empty_after = clean_data(df)  # Dodano `empty_before`

        rows_after = df_cleaned.shape[0]
        changed_data_percentage = ((empty_before - empty_after) / (rows_before * len(df.columns))) * 100 if empty_before > 0 else 0
        deleted_data_percentage = ((rows_before - rows_after) / rows_before) * 100 if rows_before > 0 else 0

        logger.info(f"Usunięto {rows_before - rows_after} wierszy podczas czyszczenia.")
        logger.info(f"Uzupełniono {empty_before - empty_after} wartości brakujących.")

        df_standardized = standardize_data(df_cleaned)
        # update_google_sheet(df_standardized)

        with open("report.txt", "w") as f:
            f.write(f"Procent danych zmienionych: {changed_data_percentage:.2f}%\n")
            f.write(f"Procent danych usuniętych: {deleted_data_percentage:.2f}%\n")
    else:
        logger.error("Nie podano żadnych opcji. Użyj --upload lub --standardize.")

if __name__ == '__main__':
    main()
