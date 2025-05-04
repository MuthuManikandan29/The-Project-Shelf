import streamlit as st
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Load the breast cancer dataset
breast_cancer_dataset = load_breast_cancer()

# Create a DataFrame
data_frame = pd.DataFrame(breast_cancer_dataset.data, columns=breast_cancer_dataset.feature_names)
data_frame['label'] = breast_cancer_dataset.target

# Splitting data into training and testing sets
X = data_frame.drop(columns='label', axis=1)
Y = data_frame['label']
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)

# Train the Logistic Regression model
model = LogisticRegression(max_iter=5000)
model.fit(X_train, Y_train)

# Streamlit App UI
st.title("🔬 Breast Cancer Prediction App")
st.write("Enter **30 feature values** as a comma-separated list (e.g., `13.53, 10.94, 87.91, ...`) and click **Predict**.")

# Display feature names in a compact format
with st.expander("📌 **Click here to see the required feature names**"):
    st.write("""
    - **Mean Values**: Radius, Texture, Perimeter, Area, Smoothness, Compactness, Concavity, Concave Points, Symmetry, Fractal Dimension  
    - **Error Values**: Radius, Texture, Perimeter, Area, Smoothness, Compactness, Concavity, Concave Points, Symmetry, Fractal Dimension  
    - **Worst Values**: Radius, Texture, Perimeter, Area, Smoothness, Compactness, Concavity, Concave Points, Symmetry, Fractal Dimension  
    """)

# Input box for all feature values in a single string
input_data_str = st.text_input("📥 **Enter feature values (30 comma-separated numbers):**")

# Prediction Button
if st.button("🔍 Predict"):
    if input_data_str:
        try:
            # Convert input string to a list of floats
            input_data_list = [float(value) for value in input_data_str.split(',')]
            
            # Ensure the correct number of features
            if len(input_data_list) == len(breast_cancer_dataset.feature_names):
                input_data_array = np.array(input_data_list).reshape(1, -1)
                prediction = model.predict(input_data_array)

                # Display prediction result
                if prediction[0] == 1:
                    st.success("✅ The breast cancer is **Benign**.")
                else:
                    st.error("⚠️ The breast cancer is **Malignant**.")
            else:
                st.warning(f"⚠️ Please enter exactly {len(breast_cancer_dataset.feature_names)} values.")
        except ValueError:
            st.warning("⚠️ Please enter valid numerical values, separated by commas.")
    else:
        st.warning("⚠️ Please enter the feature values.")
