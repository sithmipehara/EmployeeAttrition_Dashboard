import streamlit as st
import pandas as pd

# Load dataset from GitHub
data_url = "https://raw.githubusercontent.com/sithmipehara/EmployeeAttrition_Dashboard/refs/heads/main/train.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(data_url)
    df = df.iloc[:, 1:]  # Remove the first column (ID column)
    return df

# Load the data
data = load_data()

# Calculate metrics
num_data_points = data.shape[0]
num_categorical_vars = len(data.select_dtypes(include=['object']).columns)
num_numerical_vars = len(data.select_dtypes(include=['number']).columns)
response_variable = 'Attrition'  # Assuming 'Attrition' is the response variable

# Create a single column for boxes
col1 = st.container()

with col1:
    st.markdown(
        f"""
        <div style="background-color: #2b2b55; padding: 20px; border-radius: 10px;">
            <h3 style="color: white;">Number of Data Points</h3>
            <p style="color: white;">{num_data_points}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        f"""
        <div style="background-color: #2b2b55; padding: 20px; border-radius: 10px; margin-top: 10px;">
            <h3 style="color: white;">Number of Categorical Variables</h3>
            <p style="color: white;">{num_categorical_vars}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        f"""
        <div style="background-color: #2b2b55; padding: 20px; border-radius: 10px; margin-top: 10px;">
            <h3 style="color: white;">Number of Numerical Variables</h3>
            <p style="color: white;">{num_numerical_vars}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        f"""
        <div style="background-color: #2b2b55; padding: 20px; border-radius: 10px; margin-top: 10px;">
            <h3 style="color: white;">Response Variable</h3>
            <p style="color: white;">{response_variable}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
