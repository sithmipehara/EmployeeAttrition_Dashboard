import streamlit as st
import pandas as pd
import plotly.express as px

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
    # Donut Chart for Response Variable
    response_counts = data[response_variable].value_counts().reset_index()
    response_counts.columns = [response_variable, 'count']
    
    # Create a donut chart using Plotly
    fig = px.pie(response_counts, 
                 values='count', 
                 names=response_variable,
                 hole=0.5,
                 color_discrete_sequence=['#00b3b3', '#ff6666'])

    # Update layout to match dashboard theme
    fig.update_layout(
        title_text='Response Variable Distribution',
        paper_bgcolor='#2b2b55',
        plot_bgcolor='#2b2b55',
        font_color='white'
    )

    st.markdown(
        """
        <div style="background-color: #2b2b55; padding: 20px; border-radius: 10px;">
            <h6 style="color: white;">Response Variable Distribution</h6>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Display the donut chart in Streamlit
    st.plotly_chart(fig)

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
