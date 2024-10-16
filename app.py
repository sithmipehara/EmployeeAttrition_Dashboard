import streamlit as st
import pandas as pd
import altair as alt

# Load the data
data_url = "https://raw.githubusercontent.com/sithmipehara/EmployeeAttrition_Dashboard/refs/heads/main/train.csv"
df = pd.read_csv(data_url).iloc[:, 1:]  # Remove the first column (ID)

# Set page configuration
st.set_page_config(page_title="Filled Positions Dashboard", layout="wide")

# Dashboard title


# Header metrics
num_data_points = df.shape[0]
num_categorical = df.select_dtypes(include=['object']).shape[1]
num_numerical = df.select_dtypes(include=['int64', 'float64']).shape[1]
response_variable = "Attrition"

# Display the metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("No. of Data Points", num_data_points)
col2.metric("No. of Categorical Variables", num_categorical)
col3.metric("No. of Numerical Variables", num_numerical)
col4.metric("Response Variable", response_variable)

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

# Bar Chart for Selected Categorical Variable
st.markdown("## Categorical Variable Distribution")
cat_data = df[cat_var].value_counts().reset_index()
cat_data.columns = [cat_var, "Count"]
cat_chart = alt.Chart(cat_data).mark_bar().encode(
    x=alt.X(cat_var, sort="-y"),
    y="Count:Q",
    tooltip=[cat_var, "Count"]
).properties(width=300, height=300)

# Histogram for Selected Numerical Variable
st.markdown("## Numerical Variable Distribution")
num_chart = alt.Chart(df).mark_bar().encode(
    x=alt.X(num_var, bin=True),
    y='count()',
    tooltip=[num_var, 'count()']
).properties(width=300, height=300)

# Layout for visualizations
col1, col2, col3 = st.columns(3)
col1.markdown("### Response Variable (Attrition)")
col1.altair_chart(response_chart, use_container_width=True)

col2.markdown("### Categorical Variable Distribution")
col2.altair_chart(cat_chart, use_container_width=True)

col3.markdown("### Numerical Variable Distribution")
col3.altair_chart(num_chart, use_container_width=True)
