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
    st.markdown(f"<div style='background-color: {background_color}; padding: 20px; border-radius: 10px;height: 155px;'>"
                f"<h5 style='text-align: center; color: #FFFFFF;'>Number of Data Points</h5>"
                f"<h2 style='text-align: center; color: #FFFFFF;'>{num_data_points}</h2></div>", 
                unsafe_allow_html=True)

with col2:
    st.markdown(f"<div style='background-color: {background_color}; padding: 20px; border-radius: 10px;height: 155px;'>"
                f"<h5 style='text-align: center; color: #FFFFFF;'>Number of Categorical Variables</h5>"
                f"<h2 style='text-align: center; color: #FFFFFF;'>{num_categorical_vars}</h2></div>", 
                unsafe_allow_html=True)

with col3:
    st.markdown(f"<div style='background-color: {background_color}; padding: 20px; border-radius: 10px;height: 155px;'>"
                f"<h5 style='text-align: center; color: #FFFFFF;'>Number of Numerical Variables</h5>"
                f"<h2 style='text-align: center; color: #FFFFFF;'>{num_numerical_vars}</h2></div>", 
                unsafe_allow_html=True)

with col4:
    st.markdown(f"<div style='background-color: {background_color}; padding: 20px; border-radius: 10px; height: 155px;'>"
                f"<h5 style='text-align: center; color: #FFFFFF;'>Response Variable</h5>"
                f"<h2 style='text-align: center; color: #FFFFFF;'>{response_variable}</h2></div>", 
                unsafe_allow_html=True)

# Add space between the header and charts
st.write("---")

# Create three charts in one row
col5, col6, col7 = st.columns(3)

# Chart 1: Response Variable - Donut Chart
with col5:
    st.markdown("<h4 style='text-align: center;'>Attrition Distribution</h4>", unsafe_allow_html=True)
    st.write("---")
    attrition_counts = df['Attrition'].value_counts().reset_index()
    attrition_counts.columns = ['Attrition', 'Count']
    
    donut_chart = alt.Chart(attrition_counts).mark_arc(innerRadius=70).encode(
        theta=alt.Theta(field='Count', type='quantitative'),
        color=alt.Color(field='Attrition', type='nominal', legend=None),
        tooltip=['Attrition', 'Count']
    ).properties(width=300, height=300)
    
    st.altair_chart(donut_chart, use_container_width=True)

# Combined Filter for Categorical Variables - Bar Chart and Stacked Bar Chart
with col6:
    st.markdown("<h4 style='text-align: center;'>Categorical Variable Distribution</h4>", unsafe_allow_html=True)
    
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    categorical_cols.remove('Attrition')  # Remove Attrition from options
    
    selected_cat_var = st.selectbox("", categorical_cols)
    
    cat_counts = df[selected_cat_var].value_counts().reset_index()
    cat_counts.columns = [selected_cat_var, 'Count']
    
    bar_chart = alt.Chart(cat_counts).mark_bar().encode(
        x=alt.X(selected_cat_var, sort='-y'),
        y='Count',
        color=alt.Color(selected_cat_var, legend=None),
        tooltip=[selected_cat_var, 'Count']
    ).properties(width=300, height=300)
    
    st.altair_chart(bar_chart, use_container_width=True)

# Stacked Bar Chart for Response vs Categorical Variable
with col7:
    st.markdown("<h5 style='text-align: center;color: #2BCDD5;'>Categorical Variable Vs Response Variable</h5>", unsafe_allow_html=True)
    st.write("---")
    st.write("---")

    stacked_data = df.groupby([selected_cat_var, 'Attrition']).size().reset_index(name='Count')
    
    stacked_bar_chart = alt.Chart(stacked_data).mark_bar().encode(
        x=alt.X(selected_cat_var),
        y='Count',
        color=alt.Color('Attrition:N', legend=None),
        tooltip=[selected_cat_var, 'Attrition', 'Count']
    ).properties(width=300, height=300).configure_mark(
        opacity=0.8,
        strokeWidth=0
    )
    
    st.altair_chart(stacked_bar_chart, use_container_width=True)

# Add space between the first and second rows of charts
st.write("---")

# Create two new charts in another row
col8, col9 , col10= st.columns(3)

# Combined Filter for Numerical Variables - Histogram and Box Plot
with col9:
    st.markdown("<h4 style='text-align: center;'>Numerical Variable Distribution</h4>", unsafe_allow_html=True)
    
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    selected_num_var = st.selectbox("", numerical_cols)
    
    histogram = alt.Chart(df).mark_bar().encode(
        x=alt.X(selected_num_var, bin=True),
        y='count()',
        tooltip=[selected_num_var, 'count()']
    ).properties(width=300, height=300)
    
    st.altair_chart(histogram, use_container_width=True)

# Box Plot for Response vs Numerical Variable using the same numerical variable filter
with col10:
    st.markdown("<h5 style='text-align: center;color: #2BCDD5;'>Numerical Variable Vs Response Variable</h5>", unsafe_allow_html=True)
    st.write("---")
    st.write("---")
    
    box_plot = alt.Chart(df).mark_boxplot().encode(
        x=alt.X('Attrition:N'),
        y=alt.Y(selected_num_var),
        tooltip=['Attrition', selected_num_var]
    ).properties(width=300, height=300)
    
    st.altair_chart(box_plot, use_container_width=True)

st.write("### Additional Insights")
st.write("This dashboard visualizes employee attrition data, providing insights into various attributes.")
