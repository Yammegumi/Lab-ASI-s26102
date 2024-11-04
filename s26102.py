# train.py
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


# Funkcja do generowania zbioru danych z dwiema klasami
def generate_data():
    cluster_sizes = np.random.randint(50, 101, size=2)
    cluster_centers = [np.array([5, 5]), np.array([-5, -5])]

    cluster_1 = np.random.randn(cluster_sizes[0], 2) + cluster_centers[0]
    cluster_2 = np.random.randn(cluster_sizes[1], 2) + cluster_centers[1]

    labels_1 = np.zeros(cluster_sizes[0])
    labels_2 = np.ones(cluster_sizes[1])

    X = np.vstack([cluster_1, cluster_2])
    y = np.concatenate([labels_1, labels_2])

    return X, y


# Funkcja do trenowania modelu i zapisywania dokładności
def train_and_evaluate():
    X, y = generate_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    classifier = LogisticRegression()
    classifier.fit(X_train, y_train)

    test_accuracy = classifier.score(X_test, y_test) * 100
    print(f"Model accuracy: {test_accuracy:.2f}%")

    # Zapisanie dokładności modelu do pliku
    with open('accuracy.txt', 'w') as file:
        file.write(f"Model accuracy: {test_accuracy:.2f}%\n")


if __name__ == "__main__":
    train_and_evaluate()
