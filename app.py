import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set the theme to dark
st.set_page_config(page_title="Employee Attrition Dashboard", layout="wide", initial_sidebar_state="expanded")

# Load dataset from GitHub
data_url = "https://raw.githubusercontent.com/sithmipehara/EmployeeAttrition_Dashboard/refs/heads/main/train.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(data_url)
    # Remove the first column (ID column)
    df = df.iloc[:, 1:]  # Assuming the first column is the ID column
    return df

# Load data
df = load_data()

# Calculate metrics for display in containers
num_data_points = df.shape[0]
num_categorical_vars = df.select_dtypes(include=['object']).shape[1]
num_numerical_vars = df.select_dtypes(include=['int64', 'float64']).shape[1]
response_variable = "Attrition"

# Create a horizontal row with four containers
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

# Create three charts in one row
col5, col6, col7 = st.columns(3)

# Chart 1: Response Variable - Pie Chart
with col5:
    st.subheader("Attrition Distribution")
    attrition_counts = df['Attrition'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(attrition_counts, labels=attrition_counts.index, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig1)

# Chart 2: Categorical Variables - Bar Chart with Filter
with col6:
    st.subheader("Categorical Variable Distribution")
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    selected_cat_var = st.selectbox("Select Categorical Variable:", categorical_cols)
    
    cat_counts = df[selected_cat_var].value_counts()
    fig2, ax2 = plt.subplots()
    ax2.bar(cat_counts.index, cat_counts.values)
    ax2.set_title(selected_cat_var)
    ax2.set_xlabel(selected_cat_var)
    ax2.set_ylabel("Count")
    plt.xticks(rotation=45)
    st.pyplot(fig2)

# Chart 3: Numerical Variables - Histogram with Filter
with col7:
    st.subheader("Numerical Variable Distribution")
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    selected_num_var = st.selectbox("Select Numerical Variable:", numerical_cols)
    
    fig3, ax3 = plt.subplots()
    ax3.hist(df[selected_num_var], bins=30, color='blue', alpha=0.7)
    ax3.set_title(f"Histogram of {selected_num_var}")
    ax3.set_xlabel(selected_num_var)
    ax3.set_ylabel("Frequency")
    st.pyplot(fig3)

st.write("### Additional Insights")
st.write("This dashboard visualizes employee attrition data, providing insights into various attributes.")
