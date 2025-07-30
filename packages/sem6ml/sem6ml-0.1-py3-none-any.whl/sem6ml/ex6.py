# exercise1.py
import inspect
import sys

print("=== Code of sem6ml.exercise6 ===")
print(inspect.getsource(sys.modules[__name__]))

def run():
    print("Running K-Nearest Neighbors (K-NN) Algorithm...")

    import numpy as np
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.metrics import accuracy_score

    # Extended dataset
    data = {
        'X1': [2, 4, 4, 6, 8, 1, 3, 7, 9, 5, 6, 2],
        'X2': [4, 6, 4, 2, 4, 5, 7, 3, 5, 6, 2, 3],
        'Class': ['A', 'A', 'B', 'B', 'B', 'A', 'A', 'B', 'B', 'A', 'B', 'A']
    }
    df = pd.DataFrame(data)

    # Features and Labels
    X = df[['X1', 'X2']]
    y = df['Class']

    # Splitting into train and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define KNN model with reduced neighbors
    knn = KNeighborsClassifier(n_neighbors=6)
    knn.fit(X_train, y_train)

    # Prediction
    y_pred = knn.predict(X_test)
    print("Predicted:", y_pred)

    # Accuracy
    print("Accuracy:", accuracy_score(y_test, y_pred))