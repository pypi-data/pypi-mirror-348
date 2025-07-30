# exercise1.py
import inspect
import sys

print("=== Code of sem6ml.exercise8 ===")
print(inspect.getsource(sys.modules[__name__]))

def run():
    print("Running Decision Tree Algorithm...")
    
    # Original Decision Tree implementation code
    import numpy as np
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeClassifier, plot_tree
    from sklearn.metrics import accuracy_score
    import matplotlib.pyplot as plt

    # Sample dataset
    data = {
        'Age': ['<=30', '<=30', '31-40', '>40', '>40'],
        'Income': ['High', 'High', 'High', 'Medium', 'Low'],
        'Student': ['No', 'No', 'No', 'No', 'Yes'],
        'Credit_Rating': ['Fair', 'Excellent', 'Fair', 'Fair', 'Fair'],
        'Class': ['No', 'No', 'Yes', 'Yes', 'Yes']
    }
    df = pd.DataFrame(data)
    
    # Convert categorical variables into numerical format
    df = pd.get_dummies(df, columns=['Age', 'Income', 'Student', 'Credit_Rating'], drop_first=True)
    
    # Features and Labels
    X = df.drop(columns=['Class'])
    y = df['Class']
    
    # Splitting into train and test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Define Decision Tree model
    dt_model = DecisionTreeClassifier(criterion='entropy', random_state=42)
    dt_model.fit(X_train, y_train)
    
    # Prediction
    y_pred = dt_model.predict(X_test)
    
    # Accuracy
    print("\nModel Accuracy:", accuracy_score(y_test, y_pred))
    
    # Plot Decision Tree
    plt.figure(figsize=(10,6))
    plot_tree(dt_model, 
              filled=True, 
              feature_names=X.columns, 
              class_names=['No', 'Yes'])
    plt.title("Decision Tree Visualization")
    plt.show()