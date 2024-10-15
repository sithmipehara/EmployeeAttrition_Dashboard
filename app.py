import streamlit as st
import pandas as pd
import altair as alt

# Set the theme to dark
st.set_page_config(page_title="Employee Attrition Dashboard", layout="wide", initial_sidebar_state="expanded")

# Load dataset from GitHub
data_url = "https://raw.githubusercontent.com/sithmipehara/EmployeeAttrition_Dashboard/refs/heads/main/train.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(data_url)
    df = df.iloc[:, 1:]  # Remove the first column (ID column)
    return df

# Load data
df = load_data()

# Calculate metrics for display in containers
num_data_points = df.shape[0]
num_categorical_vars = df.select_dtypes(include=['object']).shape[1] - 1  # Exclude Attrition
num_numerical_vars = df.select_dtypes(include=['int64', 'float64']).shape[1]
response_variable = "Attrition"

# Create a horizontal row with four containers
col1, col2, col3, col4 = st.columns(4)

# Define background colors for the containers
background_color = "#2c2c2e" 

with col1:
    st.markdown(f"<div style='background-color: {background_color}; padding: 20px; border-radius: 10px;'>"
                f"<h5 style='text-align: center; color: #FFFFFF;'>Number of Data Points</h5>"
                f"<h2 style='text-align: center; color: #FFFFFF;'>{num_data_points}</h2></div>", 
                unsafe_allow_html=True)

with col2:
    st.markdown(f"<div style='background-color: {background_color}; padding: 20px; border-radius: 10px;'>"
                f"<h5 style='text-align: center; color: #FFFFFF;'>Number of Categorical Variables</h5>"
                f"<h2 style='text-align: center; color: #FFFFFF;'>{num_categorical_vars}</h2></div>", 
                unsafe_allow_html=True)

with col3:
    st.markdown(f"<div style='background-color: {background_color}; padding: 20px; border-radius: 10px;'>"
                f"<h5 style='text-align: center; color: #FFFFFF;'>Number of Numerical Variables</h5>"
                f"<h2 style='text-align: center; color: #FFFFFF;'>{num_numerical_vars}</h2></div>", 
                unsafe_allow_html=True)

with col4:
    st.markdown(f"<div style='background-color: {background_color}; padding: 20px; border-radius: 10px; height: 10px'>"
                f"<h5 style='text-align: center; color: #FFFFFF;'>Response Variable</h5>"
                f"<h2 style='text-align: center; color: #FFFFFF;'>{response_variable}</h2></div>", 
                unsafe_allow_html=True)

# Add space between the header and charts
st.write("---")

# Create three charts in one row with background colors
col5, col6, col7 = st.columns(3)

chart_background_color = "#C00000"  # Red for charts

# Chart 1: Response Variable - Donut Chart
with col5:
    st.markdown(f"<div style='background-color: {chart_background_color}; padding: 20px; border-radius: 10px;'>"
                f"<h4 style='text-align: center; color: #FFFFFF;'>Attrition Distribution</h4></div>", 
                unsafe_allow_html=True)
    
    attrition_counts = df['Attrition'].value_counts().reset_index()
    attrition_counts.columns = ['Attrition', 'Count']
    
    donut_chart = alt.Chart(attrition_counts).mark_arc(innerRadius=70).encode(
        theta=alt.Theta(field='Count', type='quantitative'),
        color=alt.Color(field='Attrition', type='nominal', legend=None),
        tooltip=['Attrition', 'Count']
    ).properties(width=300, height=300)
    
    st.altair_chart(donut_chart, use_container_width=True)

# Chart 2: Categorical Variables - Bar Chart with Filter (excluding Attrition)
with col6:
    st.markdown(f"<div style='background-color: {chart_background_color}; padding: 20px; border-radius: 10px;'>"
                f"<h4 style='text-align: center; color: #FFFFFF;'>Categorical Variable Distribution</h4></div>", 
                unsafe_allow_html=True)
    
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    categorical_cols.remove('Attrition')  # Remove Attrition from options
    
    selected_cat_var = st.selectbox("Select Categorical Variable:", categorical_cols)
    
    cat_counts = df[selected_cat_var].value_counts().reset_index()
    cat_counts.columns = [selected_cat_var, 'Count']
    
    bar_chart = alt.Chart(cat_counts).mark_bar().encode(
        x=alt.X(selected_cat_var, sort='-y'),
        y='Count',
        color=alt.Color(selected_cat_var, legend=None),
        tooltip=[selected_cat_var, 'Count']
    ).properties(width=300, height=300)
    
    st.altair_chart(bar_chart, use_container_width=True)

# Chart 3: Numerical Variables - Histogram with Filter
with col7:
    st.markdown(f"<div style='background-color: {chart_background_color}; padding: 20px; border-radius: 10px;'>"
                f"<h4 style='text-align: center; color: #FFFFFF;'>Numerical Variable Distribution</h4></div>", 
                unsafe_allow_html=True)
    
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    selected_num_var = st.selectbox("Select Numerical Variable:", numerical_cols)
    
    histogram = alt.Chart(df).mark_bar().encode(
        x=alt.X(selected_num_var, bin=True),
        y='count()',
        tooltip=[selected_num_var, 'count()']
    ).properties(width=300, height=300)
    
    st.altair_chart(histogram, use_container_width=True)

st.write("### Additional Insights")
st.write("This dashboard visualizes employee attrition data, providing insights into various attributes.")
