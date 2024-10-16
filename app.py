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

        /* Style for individual metric boxes */
        .metric-box {
            padding: 20px;
            border-radius: 8px;
            color: white;
            text-align: center;
            font-size: 16px;
            font-weight: bold;
        }
        
        .box1 { background-color: #b3d9ff;color: #000000; }
        .box2 { background-color: #66b3ff;color: #000000; }
        .box3 { background-color: #ff6666; color:#000000;}
        .box4 { background-color: #ff9999;color: #000000; }
        
        /* Color Scheme for Main Title */
        .title {
            color: #FFFFFF;
            font-size: 30px;
            font-weight: bold;
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)

# Dashboard title

# Header metrics
num_data_points = df.shape[0]
num_categorical = df.select_dtypes(include='object').shape[1]
num_numerical = df.select_dtypes(include='number').shape[1]
response_variable = "Attrition"

# Display the metrics
col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"<div class='metric-box box1'>No. of Data Points<br><span style='font-size: 24px;'>{num_data_points}</span></div>", unsafe_allow_html=True)
col2.markdown(f"<div class='metric-box box2'>No. of Categorical Variables<br><span style='font-size: 24px;'>{num_categorical}</span></div>", unsafe_allow_html=True)
col3.markdown(f"<div class='metric-box box3'>No. of Numerical Variables<br><span style='font-size: 24px;'>{num_numerical}</span></div>", unsafe_allow_html=True)
col4.markdown(f"<div class='metric-box box4'>Response Variable<br><span style='font-size: 24px;'>{response_variable}</span></div>", unsafe_allow_html=True)

st.write(" ")

# Sidebar filters
st.sidebar.header("Filters")
cat_var = st.sidebar.selectbox("Select Categorical Variable", options=df.select_dtypes(include='object').columns)
num_var = st.sidebar.selectbox("Select Numerical Variable", options=df.select_dtypes(include='number').columns)

# Response Variable Distribution (Donut Chart with Center Text)
response_data = df["Attrition"].value_counts().reset_index()
response_data.columns = ["Attrition", "Count"]

# Donut chart base
donut_chart = alt.Chart(response_data).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="Count", type="quantitative"),
    color=alt.Color(field="Attrition", type="nominal", scale=alt.Scale(scheme="tableau20")),
    tooltip=["Attrition", "Count"]
).properties(width=200, height=200)

# Center text overlay
total_count = response_data["Count"].sum()
text = alt.Chart(pd.DataFrame({'text': [total_count]})).mark_text(
    text=str(total_count),
    size=28,
    color='white',
    dx=0, dy=-10
).encode(
    text='text:N'
)

# Labels for each segment of the donut
segment_labels = donut_chart.mark_text(radius=90, size=14, color="white").encode(
    text=alt.Text('Count:Q')
)

# Combine the donut chart with center text and segment labels
response_donut_chart = donut_chart + center_text + segment_labels

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
col1.markdown("<h4 style='text-align: center;'>Response variable Distribution</h4>", unsafe_allow_html=True)
col1.altair_chart(response_donut_chart, use_container_width=True)

col2.markdown("<h4 style='text-align: center;'>Categorical Variables Distribution</h4>", unsafe_allow_html=True)
col2.altair_chart(cat_chart, use_container_width=True)

col3.markdown("<h4 style='text-align: center;'>Numerical Variables Distribution</h4>", unsafe_allow_html=True)
col3.altair_chart(num_chart, use_container_width=True)

# Additional Row for New Graphs
col4, col5, col6 = st.columns(3)
col4.markdown("<h4 style='text-align: center;'>Data Preview</h4>", unsafe_allow_html=True)
col4.dataframe(df.head(), height=300)

col5.markdown("<h4 style='text-align: center;'>Response vs Categorical Variables</h4>", unsafe_allow_html=True)
col5.altair_chart(stacked_cat_chart, use_container_width=True)

col6.markdown("<h4 style='text-align: center;'>Response vs Numerical Variables</h4>", unsafe_allow_html=True)
col6.altair_chart(box_plot, use_container_width=True)

# Run the app with: streamlit run app.py
