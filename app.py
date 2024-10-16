import pandas as pd
import streamlit as st
import plotly.express as px

# Load the dataset
data_url = "https://raw.githubusercontent.com/sithmipehara/EmployeeAttrition_Dashboard/refs/heads/main/train.csv"
df = pd.read_csv(data_url)

# Get basic statistics
num_data_points = df.shape[0]
num_categorical = df.select_dtypes(include=['object']).shape[1]
num_numerical = df.select_dtypes(include=['number']).shape[1]
response_variable = 'Attrition'

# Set up the Streamlit app
st.title("Employee Attrition Dashboard")

# Top container with statistics
st.header("Dataset Overview")
st.write(f"No. of Data Points: {num_data_points}")
st.write(f"No. of Categorical Variables: {num_categorical}")
st.write(f"No. of Numerical Variables: {num_numerical}")
st.write(f"Response Variable: {response_variable}")

# Filters for categorical variables
categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
selected_categorical = st.selectbox("Select a categorical variable", categorical_columns)

# Bar chart for selected categorical variable
bar_fig = px.bar(df, x=selected_categorical, color=response_variable, title=f'Bar Chart of {selected_categorical}')
st.plotly_chart(bar_fig)

# Filters for numerical variables
numerical_columns = df.select_dtypes(include=['number']).columns.tolist()
selected_numerical = st.selectbox("Select a numerical variable", numerical_columns)

# Histogram for selected numerical variable
hist_fig = px.histogram(df, x=selected_numerical, color=response_variable, title=f'Histogram of {selected_numerical}')
st.plotly_chart(hist_fig)

# Horizontal stacked bar chart for response vs categorical variable
response_categorical_fig = px.histogram(df, x=selected_categorical, color=response_variable, barmode='stack', title=f'Response vs {selected_categorical}')
st.plotly_chart(response_categorical_fig)

# Box plot for response vs numerical variable
response_numerical_fig = px.box(df, x=response_variable, y=selected_numerical, title=f'Response vs {selected_numerical}')
st.plotly_chart(response_numerical_fig)

# Donut chart for response variable
donut_fig = px.pie(df, names=response_variable, values=df[response_variable].value_counts(), hole=0.3,
                   title='Donut Chart of Response Variable')
st.plotly_chart(donut_fig)
