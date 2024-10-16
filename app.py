import streamlit as st
import pandas as pd
import altair as alt

# Load the data
data_url = "https://raw.githubusercontent.com/sithmipehara/EmployeeAttrition_Dashboard/refs/heads/main/train.csv"
df = pd.read_csv(data_url).iloc[:, 1:]  # Remove the first column (ID)

# Set page configuration
st.set_page_config(page_title="Employee Attrition Dashboard", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        /* Set Background color */
        .reportview-container {
            background-color: #1A1A3D;
        }
        .sidebar .sidebar-content {
            background-color: #1A1A3D;
        }
        
        /* Style for metric boxes */
        .metric-container {
            background-color: #27566B;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
            color: #FFFFFF;
            text-align: center;
        }
        
        /* Color Scheme for Main Title */
        .title {
            color: #FFFFFF;
            font-size: 30px;
            font-weight: bold;
            text-align: center;
        }
        
        /* Style for Altair Charts */
        .chart-container {
            background-color: #2D2F5F;
            padding: 15px;
            border-radius: 10px;
        }
        
        /* Adjusting Data Preview Table Style */
        .dataframe {
            background-color: #2D2F5F;
            color: #FFFFFF;
            border-radius: 5px;
        }
        
        /* Filter Header */
        .sidebar .sidebar-content .css-1aumxhk {
            color: #FFFFFF;
        }
    </style>
    """, unsafe_allow_html=True)

# Dashboard title
st.markdown("<h1 class='title'>Employee Attrition Dashboard</h1>", unsafe_allow_html=True)

# Header metrics
num_data_points = df.shape[0]
num_categorical = df.select_dtypes(include='object').shape[1]
num_numerical = df.select_dtypes(include='number').shape[1]
response_variable = "Attrition"

# Display the metrics
st.markdown("<div class='metric-container'>No. of Data Points: " + str(num_data_points) + "</div>", unsafe_allow_html=True)
st.markdown("<div class='metric-container'>No. of Categorical Variables: " + str(num_categorical) + "</div>", unsafe_allow_html=True)
st.markdown("<div class='metric-container'>No. of Numerical Variables: " + str(num_numerical) + "</div>", unsafe_allow_html=True)
st.markdown("<div class='metric-container'>Response Variable: " + response_variable + "</div>", unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("Filters")
cat_var = st.sidebar.selectbox("Select Categorical Variable", options=df.select_dtypes(include='object').columns)
num_var = st.sidebar.selectbox("Select Numerical Variable", options=df.select_dtypes(include='number').columns)


# Response Variable Distribution (Donut Chart)
response_data = df["Attrition"].value_counts().reset_index()
response_data.columns = ["Attrition", "Count"]
response_chart = alt.Chart(response_data).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="Count", type="quantitative"),
    color=alt.Color(field="Attrition", type="nominal", scale=alt.Scale(scheme="tableau20")),
    tooltip=["Attrition", "Count"]
).properties(width=200, height=200)

# Dataset Preview
st.markdown("## Dataset Preview")
st.dataframe(df.head())

# Categorical Variable Bar Chart
cat_data = df[cat_var].value_counts().reset_index()
cat_data.columns = [cat_var, "Count"]
cat_chart = alt.Chart(cat_data).mark_bar().encode(
    x=alt.X(cat_var, sort="-y"),
    y="Count:Q",
    tooltip=[cat_var, "Count"]
).properties(width=300, height=300)

# Numerical Variable Histogram
num_chart = alt.Chart(df).mark_bar().encode(
    x=alt.X(num_var, bin=True),
    y='count()',
    tooltip=[num_var, 'count()']
).properties(width=300, height=300)

# Response vs Categorical Variable (Stacked Bar Chart)
stacked_cat_chart = alt.Chart(df).mark_bar().encode(
    y=alt.Y(cat_var, title=cat_var, sort='-x'),
    x=alt.X('count()', title='Count'),
    color=alt.Color('Attrition', scale=alt.Scale(scheme="tableau20")),
    tooltip=[cat_var, 'Attrition', 'count()']
).properties(width=300, height=300)

# Response vs Numerical Variable (Box Plot)
box_plot = alt.Chart(df).mark_boxplot().encode(
    x=alt.X("Attrition:N", title="Attrition"),
    y=alt.Y(num_var, title=num_var),
    color=alt.Color("Attrition", scale=alt.Scale(scheme="tableau20")),
    tooltip=["Attrition", num_var]
).properties(width=300, height=300)

# Layout for visualizations
col1, col2, col3 = st.columns(3)
col1.markdown("### Response Variable (Attrition)")
col1.altair_chart(response_chart, use_container_width=True)

col2.markdown("### Categorical Variable Distribution")
col2.altair_chart(cat_chart, use_container_width=True)

col3.markdown("### Numerical Variable Distribution")
col3.altair_chart(num_chart, use_container_width=True)

# Additional Row for New Graphs
col4, col5, col6 = st.columns(3)
col4.markdown("### Dataset Preview")
col4.dataframe(df.head(), height=300)

col5.markdown("### Response vs Categorical Variable")
col5.altair_chart(stacked_cat_chart, use_container_width=True)

col6.markdown("### Response vs Numerical Variable")
col6.altair_chart(box_plot, use_container_width=True)

# Run the app with: streamlit run app.py
