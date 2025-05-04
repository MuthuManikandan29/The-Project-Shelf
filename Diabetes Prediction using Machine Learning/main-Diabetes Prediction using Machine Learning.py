import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc, confusion_matrix
import matplotlib.pyplot as plt

# Loading the diabetes dataset to a pandas DataFrame
diabetes_dataset = pd.read_csv('diabetes.csv')

# Separate the data and labels
X = diabetes_dataset.drop(columns='Outcome', axis=1)
Y = diabetes_dataset['Outcome']

# Standardize the data
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Splitting the dataset into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)

# Defining the SVM classifier
classifier = svm.SVC(kernel='linear')

# Train the SVM classifier
classifier.fit(X_train, Y_train)

# Function to predict using the classifier
def predict(input_data):
    # Standardize the input data
    std_data = scaler.transform([input_data])

    # Predict
    prediction = classifier.predict(std_data)

    return prediction[0]

# Streamlit App
def main():
    st.title('Diabetes Prediction App')

    # Display some information about the dataset
    st.subheader('Dataset Information')
    st.write(diabetes_dataset.describe())

    # Interactive prediction section
    st.subheader('Predicting Diabetes')
    st.write('Enter comma-separated values (e.g., 5,6,2,9,0,25.8,0,0):')
    input_str = st.text_input('Input:')
    if input_str:
        input_data = tuple(map(float, input_str.split(',')))
        prediction = predict(input_data)

        if prediction == 0:
            st.write(f'Prediction: The person is not diabetic')
        else:
            st.write(f'Prediction: The person is diabetic')

    # Additional visualizations (if needed)
    # Example: Display accuracy metrics, confusion matrix, ROC curve, etc.
    
if __name__ == '__main__':
    main()
