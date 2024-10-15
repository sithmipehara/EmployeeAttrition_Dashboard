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
    # Remove the first column (ID column)
    df = df.iloc[:, 1:]  # Assuming the first column is the ID column
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

# Chart 1: Response Variable - Donut Chart
with col5:
    st.subheader("Attrition Distribution")
    
    attrition_counts = df['Attrition'].value_counts().reset_index()
    attrition_counts.columns = ['Attrition', 'Count']
    
    # Calculate percentages for labels
    attrition_counts['Percentage'] = (attrition_counts['Count'] / num_data_points) * 100
    
    donut_chart = alt.Chart(attrition_counts).mark_arc(innerRadius=70).encode(
        theta=alt.Theta(field='Count', type='quantitative'),
        color=alt.Color(field='Attrition', type='nominal', legend=None),
        tooltip=['Attrition', 'Count', 'Percentage:Q']
    ).properties(width=300, height=300)
    
    # Adding labels to donut chart with percentage and count
    text = donut_chart.mark_text(radius=90, size=12).encode(
        text=alt.Text('Attrition:N', format=','),
        angle=alt.Angle('Attrition:N', axis=None),
        color=alt.condition(
            alt.datum.Count > 0,
            alt.value('white'),  # Text color for visible segments
            alt.value('transparent')  # Hide text for invisible segments
        )
    )
    
    percentage_text = donut_chart.mark_text(radius=50, size=10).encode(
        text=alt.Text('Percentage:Q', format='.1f'),
        angle=alt.Angle('Attrition:N', axis=None),
        color=alt.condition(
            alt.datum.Count > 0,
            alt.value('black'),  # Text color for visible segments
            alt.value('transparent')  # Hide text for invisible segments
        )
    )
    
    st.altair_chart(donut_chart + text + percentage_text, use_container_width=True)

# Chart 2: Categorical Variables - Bar Chart with Filter (excluding Attrition)
with col6:
    st.subheader("Categorical Variable Distribution")
    
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
    st.subheader("Numerical Variable Distribution")
    
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
