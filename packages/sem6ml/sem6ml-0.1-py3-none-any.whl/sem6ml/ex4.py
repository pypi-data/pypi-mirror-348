# exercise1.py
import inspect
import sys

print("=== Code of sem6ml.exercise4 ===")
print(inspect.getsource(sys.modules[__name__]))

def run():
    print("Running Linear Regression on Experience-Salary Data...")
    
    # Import required libraries
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error

    # Prepare the data
    experience = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)
    salary = np.array([40000, 43000, 50000, 57000, 60000])
    
    data = pd.DataFrame({
        'Experience': experience.flatten(),
        'Salary': salary
    })

    # Train the model
    X = data[['Experience']]
    y = data['Salary']
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Make predictions
    y_pred = model.predict(X)
    
    # Display results
    print(f"\nRegression Equation: Salary = {model.intercept_:.2f} + {model.coef_[0]:.2f}*Experience")
    print(f"Mean Squared Error: {mean_squared_error(y, y_pred):.2f}")
    
    # Plot the results
    plt.figure(figsize=(8, 5))
    plt.scatter(X, y, color='blue', label='Actual Data')
    plt.plot(X, y_pred, color='red', label='Regression Line')
    plt.xlabel('Years of Experience')
    plt.ylabel('Salary')
    plt.title('Linear Regression: Experience vs Salary')
    plt.legend()
    plt.grid(True)
    plt.show()