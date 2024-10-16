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

# Create two columns for the new layout
col1, col2 = st.columns(2)

# First column: Metrics containers stacked vertically
with col1:
    st.markdown("<h5 style='text-align: center;'>Number of Data Points</h5>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>{num_data_points}</h2>", unsafe_allow_html=True)

    st.markdown("<h5 style='text-align: center;'>Number of Categorical Variables</h5>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>{num_categorical_vars}</h2>", unsafe_allow_html=True)

    st.markdown("<h5 style='text-align: center;'>Number of Numerical Variables</h5>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>{num_numerical_vars}</h2>", unsafe_allow_html=True)

    st.markdown("<h5 style='text-align: center;'>Response Variable</h5>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>{response_variable}</h2>", unsafe_allow_html=True)

# Second column: Donut chart and additional metrics
with col2:
    st.markdown("<h4 style='text-align: center;'>Attrition Distribution</h4>", unsafe_allow_html=True)
    
    attrition_counts = df['Attrition'].value_counts().reset_index()
    attrition_counts.columns = ['Attrition', 'Count']
    
    donut_chart = alt.Chart(attrition_counts).mark_arc(innerRadius=70).encode(
        theta=alt.Theta(field='Count', type='quantitative'),
        color=alt.Color(field='Attrition', type='nominal', legend=None),
        tooltip=['Attrition', 'Count']
    ).properties(width=300, height=300)
    
    st.altair_chart(donut_chart, use_container_width=True)

    # Calculate counts and percentages for response variable
    total_count = attrition_counts['Count'].sum()
    for index, row in attrition_counts.iterrows():
        percentage = (row['Count'] / total_count) * 100
        st.markdown(f"<div style='text-align: center;'><strong>{row['Attrition']}</strong>: {row['Count']} ({percentage:.2f}%)</div>", unsafe_allow_html=True)

# Add space between the header and charts
st.write("---")

# Create two columns for the charts
col3, col4 = st.columns(2)

# First column of charts
with col3:
    # Chart 1: Categorical Variable Distribution
    st.markdown("<h4 style='text-align: center;'>Categorical Variable Distribution</h4>", unsafe_allow_html=True)
    
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

    # Chart 3: Numerical Variable Distribution - Histogram with Filter
    st.markdown("<h4 style='text-align: center;'>Numerical Variable Distribution</h4>", unsafe_allow_html=True)
    
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    selected_num_var = st.selectbox("Select Numerical Variable:", numerical_cols)
    
    histogram = alt.Chart(df).mark_bar().encode(
        x=alt.X(selected_num_var, bin=True),
        y='count()',
        tooltip=[selected_num_var, 'count()']
    ).properties(width=300, height=300)
    
    st.altair_chart(histogram, use_container_width=True)

# Second column of charts
with col4:
    # Chart 4: Stacked Bar Chart for Response vs Categorical Variable
    st.markdown("<h4 style='text-align: center;'>Response vs Categorical Variable</h4>", unsafe_allow_html=True)
    
    selected_cat_var_2 = st.selectbox("Select Categorical Variable for Stacked Bar Chart:", categorical_cols)
    
    stacked_data = df.groupby([selected_cat_var_2, 'Attrition']).size().reset_index(name='Count')
    
    stacked_bar_chart = alt.Chart(stacked_data).mark_bar().encode(
        x=alt.X(selected_cat_var_2),
        y='Count',
        color=alt.Color('Attrition:N', legend=None),
        tooltip=[selected_cat_var_2, 'Attrition', 'Count']
    ).properties(width=300, height=300).configure_mark(
        opacity=0.8,
        strokeWidth=0
    )
    
    st.altair_chart(stacked_bar_chart, use_container_width=True)

    # Chart 5: Box Plot for Response vs Numerical Variable
    st.markdown("<h4 style='text-align: center;'>Response vs Numerical Variable</h4>", unsafe_allow_html=True)
    
    selected_num_var_2 = st.selectbox("Select Numerical Variable for Box Plot:", numerical_cols)
    
    box_plot = alt.Chart(df).mark_boxplot().encode(
        x=alt.X('Attrition:N'),
        y=alt.Y(selected_num_var_2),
        tooltip=['Attrition', selected_num_var_2]
    ).properties(width=300, height=300)
    
    st.altair_chart(box_plot, use_container_width=True)

st.write("### Additional Insights")
st.write("This dashboard visualizes employee attrition data, providing insights into various attributes.")
