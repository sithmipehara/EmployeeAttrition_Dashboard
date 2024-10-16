import streamlit as st
import pandas as pd

# Load the dataset
data_url = "https://raw.githubusercontent.com/sithmipehara/EmployeeAttrition_Dashboard/refs/heads/main/train.csv"
df = pd.read_csv(data_url)

# Remove the first column (ID)
df.drop(df.columns[0], axis=1, inplace=True)

# Calculate required metrics
num_observations = df.shape[0]
num_categorical = df.select_dtypes(include=['object']).shape[1]
num_numerical = df.select_dtypes(exclude=['object']).shape[1]
response_variable = 'Attrition'  # Assuming 'Attrition' is the response variable

# Set the background color for the app
st.markdown("""
<style>
body {
    background-color: #111122; /* Main background color */
}
.container {
    display: flex;
    justify-content: space-between;
    margin: 5px;
}
.column {
    flex: 1; /* Equal width for columns */
    margin: 5px;
}
.container div {
    background-color: #2b2b55; /* Background color for containers */
    border: 1px solid #ccc; /* Optional border for containers */
    margin-bottom: 5px; /* Margin between containers */
    height: 100px; /* Default height for containers */
    display: flex; /* Center content horizontally and vertically */
    align-items: center;
    justify-content: center;
    color: white; /* Text color for better visibility */
}
.big-container {
    height: 150px; /* Height for the big container */
}
</style>
""", unsafe_allow_html=True)

# Create a main container with 4 columns
st.markdown('<div class="container">', unsafe_allow_html=True)

# First column with 4 equal sized containers
st.markdown('<div class="column">', unsafe_allow_html=True)
st.markdown(f'<div>No. of Observations: {num_observations}</div>', unsafe_allow_html=True)
st.markdown(f'<div>No. of Categorical Variables: {num_categorical}</div>', unsafe_allow_html=True)
st.markdown(f'<div>No. of Numerical Variables: {num_numerical}</div>', unsafe_allow_html=True)
st.markdown(f'<div>Response Variable: {response_variable}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Second column with 3 containers (first one big, other two same size)
st.markdown('<div class="column">', unsafe_allow_html=True)
st.markdown('<div class="big-container">Big Container</div>', unsafe_allow_html=True)
for i in range(2):
    st.markdown(f'<div>Container {i + 5}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Third column with 2 equal sized containers
st.markdown('<div class="column">', unsafe_allow_html=True)
for i in range(2):
    st.markdown(f'<div>Container {i + 7}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Fourth column with 2 equal sized containers
st.markdown('<div class="column">', unsafe_allow_html=True)
for i in range(2):
    st.markdown(f'<div>Container {i + 9}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Close the main container
st.markdown('</div>', unsafe_allow_html=True)
