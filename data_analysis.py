import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import os

# Ustawienie loggera
logging.basicConfig(
    filename='analysis.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    filemode='w'
)

# Sprawdzenie i utworzenie folderu na wykresy
output_dir = 'plots'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    logging.info(f'Utworzono katalog {output_dir}.')
else:
    logging.info(f'Katalog {output_dir} już istnieje.')

# Wczytanie danych
data = pd.read_csv('CollegeDistance.csv')
logging.info('Dane zostały wczytane.')

# Informacje o danych
logging.info(f'Dataset zawiera {data.shape[0]} wierszy i {data.shape[1]} kolumn.')
logging.info(f'Nazwy kolumn: {data.columns.tolist()}')

# Sprawdzenie brakujących wartości
null_counts = data.isna().sum()
missing = null_counts[null_counts > 0]
if not missing.empty:
    logging.info('Brakujące wartości w kolumnach:')
    logging.info(missing)
else:
    logging.info('Brak brakujących wartości w danych.')

# Listy kolumn numerycznych i kategorycznych
numerical_columns = ['unemp', 'wage', 'distance', 'tuition', 'education']
categorical_columns = ['gender', 'ethnicity', 'fcollege', 'mcollege', 'home', 'urban', 'income', 'region']

# Analiza zmiennych numerycznych w odniesieniu do 'score'
for feature in numerical_columns:
    try:
        data[f'{feature}_grouped'] = pd.cut(data[feature], bins=5)
        plt.figure(figsize=(9, 5))
        sns.boxplot(x=f'{feature}_grouped', y='score', data=data)
        plt.title(f'Zależność między {feature} a score')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plot_path = os.path.join(output_dir, f'{feature}_vs_score.png')
        plt.savefig(plot_path)
        plt.close()
        logging.info(f'Wykres {feature} vs score został zapisany w {plot_path}.')
    except Exception as e:
        logging.error(f'Błąd podczas tworzenia wykresu dla {feature}: {e}')

# Analiza zmiennych kategorycznych w odniesieniu do 'score'
for feature in categorical_columns:
    try:
        plt.figure(figsize=(9, 5))
        sns.boxplot(x=feature, y='score', data=data)
        plt.title(f'Zależność między {feature} a score')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plot_path = os.path.join(output_dir, f'{feature}_vs_score.png')
        plt.savefig(plot_path)
        plt.close()
        logging.info(f'Wykres {feature} vs score został zapisany w {plot_path}.')
    except Exception as e:
        logging.error(f'Błąd podczas tworzenia wykresu dla {feature}: {e}')

# Rozkłady zmiennych numerycznych
for feature in numerical_columns:
    try:
        plt.figure(figsize=(8, 4))
        sns.histplot(data[feature].dropna(), kde=True, bins=30)
        plt.title(f'Histogram zmiennej {feature}')
        plt.xlabel(feature)
        plt.ylabel('Częstość')
        plt.axvline(data[feature].mean(), color='red', linestyle='dashed', linewidth=1)
        plt.axvline(data[feature].median(), color='green', linestyle='solid', linewidth=1)
        plt.legend({'Średnia': data[feature].mean(), 'Mediana': data[feature].median()})
        plt.tight_layout()
        plot_path = os.path.join(output_dir, f'{feature}_histogram.png')
        plt.savefig(plot_path)
        plt.close()
        logging.info(f'Histogram zmiennej {feature} został zapisany w {plot_path}.')
    except Exception as e:
        logging.error(f'Błąd podczas tworzenia histogramu dla {feature}: {e}')

# Rozkłady zmiennych kategorycznych
for feature in categorical_columns:
    try:
        plt.figure(figsize=(8, 4))
        counts = data[feature].value_counts(normalize=True) * 100
        counts.plot(kind='bar')
        plt.title(f'Rozkład zmiennej {feature}')
        plt.xlabel(feature)
        plt.ylabel('Procent')
        plt.tight_layout()
        plot_path = os.path.join(output_dir, f'{feature}_barplot.png')
        plt.savefig(plot_path)
        plt.close()
        logging.info(f'Wykres rozkładu zmiennej {feature} został zapisany w {plot_path}.')
    except Exception as e:
        logging.error(f'Błąd podczas tworzenia wykresu rozkładu dla {feature}: {e}')
