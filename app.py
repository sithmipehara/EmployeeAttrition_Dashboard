import streamlit as st
import pandas as pd

# Set the theme to dark
st.set_page_config(page_title="Employee Attrition Dashboard", layout="wide", initial_sidebar_state="expanded")

# Load dataset from GitHub
data_url = "https://raw.githubusercontent.com/sithmipehara/EmployeeAttrition_Dashboard/refs/heads/main/train.csv"

@st.cache_data
def load_data():
    return pd.read_csv(data_url)

# Load data
df = load_data()

# Calculate metrics for display in containers
num_data_points = df.shape[0]
num_categorical_vars = df.select_dtypes(include=['object']).shape[1]
num_numerical_vars = df.select_dtypes(include=['int64', 'float64']).shape[1]
response_variable = "Attrition"

# Create a horizontal row with three containers
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Number of Data Points", value=num_data_points)

with col2:
    st.metric(label="Number of Categorical Variables", value=num_categorical_vars)

with col3:
    st.metric(label="Number of Numerical Variables", value=num_numerical_vars)

with col4:
    st.metric(label="Response Variable", value=response_variable)

# Add space between the header and charts
st.write("---")

# Create two charts below the containers
col5, col6 = st.columns(2)

# Example Chart 1: Distribution of Age
with col5:
    st.subheader("Age Distribution")
    st.bar_chart(df['Age'].value_counts())

# Example Chart 2: Monthly Income Distribution
with col6:
    st.subheader("Monthly Income Distribution")
    st.bar_chart(df['Monthly Income'].value_counts())

st.write("### Additional Insights")
st.write("This dashboard visualizes employee attrition data, providing insights into various attributes.")
