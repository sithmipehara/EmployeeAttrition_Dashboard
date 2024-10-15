import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title of the app
st.title("My Data Dashboard")

# Load dataset from GitHub
data_url = "https://raw.githubusercontent.com/sithmipehara/EmployeeAttrition_Dashboard/refs/heads/main/train.csv"  # Replace with your raw URL

@st.cache_data
def load_data():
    return pd.read_csv(data_url)

# Load data
df = load_data()

# Display data
st.subheader("Data Preview")
st.write(df)

# Example plot (modify according to your dataset)
if st.checkbox('Show Plot'):
    plt.figure(figsize=(10, 5))
    plt.plot(df['Column1'], df['Column2'])  # Replace with actual column names
    plt.title('Sample Plot')
    plt.xlabel('Column1')
    plt.ylabel('Column2')
    st.pyplot(plt)