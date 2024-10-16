import streamlit as st
import pandas as pd
import altair as alt

# Load dataset from GitHub
data_url = "https://raw.githubusercontent.com/sithmipehara/EmployeeAttrition_Dashboard/refs/heads/main/train.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(data_url)
    df = df.iloc[:, 1:]  # Remove the first column (ID column)
    return df

# Load the data
data = load_data()

# Calculate metrics
num_data_points = data.shape[0]
num_categorical_vars = len(data.select_dtypes(include=['object']).columns)
num_numerical_vars = len(data.select_dtypes(include=['number']).columns)
response_variable = 'Attrition'  # Assuming 'Attrition' is the response variable

# Create a single column for boxes
col1, col2 = st.columns(2)

# First Column
with col1:
    st.markdown(
        f"""
        <div style="background-color: #2b2b55; padding: 20px; border-radius: 10px;">
            <h6 style="color: white;">Number of Data Points</h6>
            <h3 style="color: white;">{num_data_points}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        f"""
        <div style="background-color: #2b2b55; padding: 20px; border-radius: 10px; margin-top: 10px;">
            <h6 style="color: white;">Number of Categorical Variables</h6>
            <h3 style="color: white;">{num_categorical_vars}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        f"""
        <div style="background-color: #2b2b55; padding: 20px; border-radius: 10px; margin-top: 10px;">
            <h6 style="color: white;">Number of Numerical Variables</h6>
            <h3 style="color: white;">{num_numerical_vars}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        f"""
        <div style="background-color: #2b2b55; padding: 20px; border-radius: 10px; margin-top: 10px;">
            <h6 style="color: white;">Response Variable</h6>
            <h6 style="color: white;">{response_variable}</h6>
        </div>
        """,
        unsafe_allow_html=True
    )

# Second Column
with col2:
    # Prepare data for Altair chart
    response_counts = data[response_variable].value_counts().reset_index()
    response_counts.columns = [response_variable, 'count']
    
    # Create a donut chart using Altair
    donut_chart = alt.Chart(response_counts).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field='count', type='quantitative'),
        color=alt.Color(field=response_variable, type='nominal', 
                        scale=alt.Scale(domain=['Left', 'Stayed'], 
                                        range=['#ff6666', '#00b3b3'])),
        tooltip=[response_variable, 'count']
    ).properties(
        title='Response Variable Distribution',
        width=300,
        height=300
    )

    # Display the donut chart in Streamlit
    st.altair_chart(donut_chart, use_container_width=True)

    # Count and Percentage for each category of response variable
    for label in response_counts[response_variable]:
        count = response_counts.loc[response_counts[response_variable] == label, 'count'].values[0]
        percentage = (count / num_data_points) * 100
        
        st.markdown(
            f"""
            <div style="background-color: #2b2b55; padding: 20px; border-radius: 10px; margin-top: 10px;">
                <h6 style="color: white;">{label} Count</h6>
                <h3 style="color: white;">{count} ({percentage:.1f}%)</h3>
            </div>
            """,
            unsafe_allow_html=True
        )
