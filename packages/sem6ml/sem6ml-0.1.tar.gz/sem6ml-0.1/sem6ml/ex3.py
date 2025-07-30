# exercise1.py
import inspect
import sys

print("=== Code of sem6ml.exercise3 ===")
print(inspect.getsource(sys.modules[__name__]))

def run():
    print("Running Naive Bayes Classification...")
    
    # Importing required libraries
    from sklearn import preprocessing
    from sklearn.naive_bayes import GaussianNB

    # Defining the dataset
    weather = ['Sunny', 'Sunny', 'Overcast', 'Rainy', 'Rainy', 'Rainy', 'Overcast', 'Sunny', 'Sunny',
               'Rainy', 'Sunny', 'Overcast', 'Overcast', 'Rainy']
    temp = ['Hot', 'Hot', 'Hot', 'Mild', 'Cool', 'Cool', 'Cool', 'Mild', 'Cool',
            'Mild', 'Mild', 'Mild', 'Hot', 'Mild']
    play = ['No', 'No', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'No', 'Yes',
            'Yes', 'Yes', 'Yes', 'Yes', 'No']

    # Creating and fitting encoders
    le = preprocessing.LabelEncoder()
    weather_encoded = le.fit_transform(weather)
    temp_encoded = le.fit_transform(temp)
    label = le.fit_transform(play)

    # Training the model
    features = list(zip(weather_encoded, temp_encoded))
    model = GaussianNB()
    model.fit(features, label)

    # Making prediction
    predicted = model.predict([[0, 2]])
    result = "Yes" if predicted[0] == 1 else "No"
    print(f"Prediction for [Overcast, Mild]: {result}")