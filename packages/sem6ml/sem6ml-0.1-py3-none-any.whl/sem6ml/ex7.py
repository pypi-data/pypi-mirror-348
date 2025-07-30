# exercise1.py
import inspect
import sys

print("=== Code of sem6ml.exercise7 ===")
print(inspect.getsource(sys.modules[__name__]))

def run():
    print("Running Support Vector Machine (SVM) Algorithm...")

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.model_selection import train_test_split
    from sklearn.svm import SVC
    from sklearn.metrics import accuracy_score

    # Sample Data
    data = {'X1': [1, 2, 3, 4, 5,6,7,8], 'X2': [3, 5, 7, 8, 9, 7,11,6], 'Class': ['A', 'A', 'B', 'B', 'B','A','B','A']}
    df = pd.DataFrame(data)

    # Features and Labels
    X = df[['X1', 'X2']]
    y = df['Class']

    # Splitting into train and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # SVM model with linear kernel
    svm_model = SVC(kernel='linear')
    svm_model.fit(X_train, y_train)

    # Prediction
    y_pred = svm_model.predict(X_test)
    print("Predicted:", y_pred)
    print("Accuracy:", accuracy_score(y_test, y_pred))

    # Visualization with hyperplane
    def plot_svm_decision_boundary(X, y, model):
        h = 0.02
        x_min, x_max = X['X1'].min() - 1, X['X1'].max() + 1
        y_min, y_max = X['X2'].min() - 1, X['X2'].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                            np.arange(y_min, y_max, h))

        Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = np.where(Z == 'A', 0, 1)
        Z = Z.reshape(xx.shape)

        plt.contourf(xx, yy, Z, alpha=0.3, cmap=plt.cm.coolwarm)
        plt.scatter(X['X1'], X['X2'], c=y.map({'A': 0, 'B': 1}),
                    cmap=plt.cm.coolwarm, edgecolors='k', s=100)

        # Plot decision boundary (hyperplane)
        w = model.coef_[0]
        b = model.intercept_[0]
        x_vals = np.linspace(x_min, x_max, 200)   
        y_vals = -(w[0] * x_vals + b) / w[1]
        plt.plot(x_vals, y_vals, 'k--', label='Decision boundary')

        # Margins
        margin = 1 / np.sqrt(np.sum(w ** 2))
        y_vals_margin_pos = y_vals + margin
        y_vals_margin_neg = y_vals - margin
        plt.plot(x_vals, y_vals_margin_pos, 'k:', label='Margin')
        plt.plot(x_vals, y_vals_margin_neg, 'k:', label='Margin')

        plt.xlabel('X1')
        plt.ylabel('X2')
        plt.title('SVM Decision Boundary with Hyperplane')
        plt.legend()
        plt.grid(True)
        plt.show()

    # Call the plotting function
    plot_svm_decision_boundary(X, y, svm_model)