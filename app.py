import streamlit as st
import pandas as pd
import altair as alt

# Load the data
data_url = "https://raw.githubusercontent.com/sithmipehara/EmployeeAttrition_Dashboard/refs/heads/main/train.csv"
df = pd.read_csv(data_url).iloc[:, 1:]  # Remove the first column (ID)

# Set page configuration
st.set_page_config(page_title="Filled Positions Dashboard", layout="wide")

# Dashboard title
st.title("Filled Positions")

# Header metrics
filled = 900
addition = 560
replacement = 200
reg = 300
temp = 400

# Display the metrics
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Filled", filled)
col2.metric("Addition", addition)
col3.metric("Replacement", replacement)
col4.metric("Reg.", reg)
col5.metric("Temp", temp)

# Sidebar filters
st.sidebar.header("Filters")
year = st.sidebar.selectbox("Year", options=["All"] + list(df["Year"].unique()))
location = st.sidebar.selectbox("Location", options=["All"] + list(df["Location"].unique()))
organization = st.sidebar.selectbox("Organization", options=["All"] + list(df["Organization"].unique()))
group = st.sidebar.multiselect("Group", options=df["Group"].unique())

# Filter data based on selections
if year != "All":
    df = df[df["Year"] == year]
if location != "All":
    df = df[df["Location"] == location]
if organization != "All":
    df = df[df["Organization"] == organization]
if group:
    df = df[df["Group"].isin(group)]

# Diversity by Organization Type (Donut Chart)
diversity_data = df["Organization Type"].value_counts().reset_index()
diversity_chart = alt.Chart(diversity_data).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="Organization Type", type="quantitative"),
    color=alt.Color(field="index", type="nominal"),
    tooltip=["index", "Organization Type"]
).properties(width=200, height=200)

# Open Position by Business Unit (Stacked Bar Chart)
business_data = df.groupby(["Business Unit", "Employment Type"]).size().reset_index(name="Count")
business_chart = alt.Chart(business_data).mark_bar().encode(
    x="Count:Q",
    y=alt.Y("Business Unit:N", sort="-x"),
    color="Employment Type:N",
    tooltip=["Business Unit", "Employment Type", "Count"]
).properties(width=250)

# Open Position by Grade (Grouped Bar Chart)
grade_data = df.groupby(["Grade", "Gender"]).size().reset_index(name="Count")
grade_chart = alt.Chart(grade_data).mark_bar().encode(
    x=alt.X("Grade:N", title=None),
    y="Count:Q",
    color="Gender:N",
    column="Gender:N",
    tooltip=["Grade", "Gender", "Count"]
).properties(width=100)

# Open Position by Job Function (Bar Chart)
job_data = df.groupby(["Job Function", "Gender"]).size().reset_index(name="Count")
job_chart = alt.Chart(job_data).mark_bar().encode(
    x="Count:Q",
    y=alt.Y("Job Function:N", sort="-x"),
    color="Gender:N",
    tooltip=["Job Function", "Gender", "Count"]
).properties(width=250)

# Open Position by Position (Tree Map)
position_data = df["Position"].value_counts().reset_index()
position_chart = alt.Chart(position_data).mark_rect().encode(
    x="index:N",
    y="Position:Q",
    color="index:N",
    tooltip=["index", "Position"]
).properties(width=200, height=200)

# Open Position by Diversity (Bar Chart)
diversity_level_data = df["Diversity Level"].value_counts().reset_index()
diversity_level_chart = alt.Chart(diversity_level_data).mark_bar().encode(
    x="Diversity Level:Q",
    y="index:N",
    color="index:N",
    tooltip=["index", "Diversity Level"]
).properties(width=200, height=200)

# Layout for visualizations
st.markdown("## Diversity by Organization Type")
st.altair_chart(diversity_chart, use_container_width=True)

st.markdown("## Open Position by Business Unit")
st.altair_chart(business_chart, use_container_width=True)

st.markdown("## Open Position by Grade")
st.altair_chart(grade_chart, use_container_width=True)

st.markdown("## Open Position by Job Function")
st.altair_chart(job_chart, use_container_width=True)

st.markdown("## Open Position by Position")
st.altair_chart(position_chart, use_container_width=True)

st.markdown("## Open Position by Diversity")
st.altair_chart(diversity_level_chart, use_container_width=True)

# Run the app with: streamlit run app.py
