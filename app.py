import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    response_counts = data[response_variable].value_counts()
    labels = response_counts.index.tolist()
    sizes = response_counts.values.tolist()
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=['#00b3b3', '#ff6666'], startangle=90, counterclock=False, autopct='%1.1f%%')
    
    # Draw a circle at the center of pie to make it look like a donut
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre_circle)
    
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    st.markdown(
        """
        <div style="background-color: #2b2b55; padding: 20px; border-radius: 10px;">
            <h6 style="color: white;">Response Variable Distribution</h6>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.pyplot(fig)

    # Count and Percentage for each category of response variable
    for label in labels:
        count = response_counts[label]
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
