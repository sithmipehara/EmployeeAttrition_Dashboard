import streamlit as st
import pandas as pd
import altair as alt

# Set the theme to dark
st.set_page_config(page_title="Employee Attrition Dashboard", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
.stApp {
    background-color: #111122;  /* Change this to your desired color */
}
[data-testid=column] {
    padding: 0; /* Removes default padding */
    margin:0; /* Removes default margin */
}
.container {
    background-color: #2b2b55; /* Dark background for metric containers */
    padding: 10px;  /* Reduced padding */
    border-radius: 0px;
    height: 160px; /* Adjust height to auto for flexibility */
    color: white; /* Text color */
    margin: 5px;  /* Reduced margin */
}
.donut-container {
    background-color: #2b2b55; /* Darker background for donut chart */
    padding: 10px;  /* Reduced padding */
    border-radius: 0px;
}
.chart-container {
    background-color: #2b2b55; /* Medium dark background for charts */
    padding: 10px;  /* Reduced padding */
    border-radius: 0px;
}
.response-container {
    background-color: #2b2b55; /* Darker background for response details */
    padding: 10px;
    border-radius: 0px;
    margin: 5px;  /* Reduced margin */
}
.stSelectbox {
    background-color: #2b2b55; /* Change this to your desired color */
    border-radius: 0px; /* Optional: rounded corners */
    padding: 10px; /* Optional: padding inside the selectbox */
}
</style>
""", unsafe_allow_html=True)

# Load dataset from GitHub
data_url = "https://raw.githubusercontent.com/sithmipehara/EmployeeAttrition_Dashboard/refs/heads/main/train.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(data_url)
    df = df.iloc[:, 1:]  # Remove the first column (ID column)
    return df

# Load data
df = load_data()

# Calculate metrics for display in containers
num_data_points = df.shape[0]
num_categorical_vars = df.select_dtypes(include=['object']).shape[1] - 1  # Exclude Attrition
num_numerical_vars = df.select_dtypes(include=['int64', 'float64']).shape[1]
response_variable = "Attrition"

# Create columns with different widths
col1, col2, col3, col4 = st.columns([1, 1.5, 2, 2])  # Adjust ratios as needed

# First column: Metrics containers stacked vertically
with col1:
    st.markdown("<div class='container'><h6 style='text-align: center;'>Number of Data Points</h6>"
                f"<h2 style='text-align: center;'>{num_data_points}</h2></div>", unsafe_allow_html=True)

    st.markdown("<div class='container'><h6 style='text-align: center;'>Number of Categorical Variables</h6>"
                f"<h2 style='text-align: center;'>{num_categorical_vars}</h2></div>", unsafe_allow_html=True)

    st.markdown("<div class='container'><h6 style='text-align: center;'>Number of Numerical Variables</h6>"
                f"<h2 style='text-align: center;'>{num_numerical_vars}</h2></div>", unsafe_allow_html=True)

    st.markdown("<div class='container'><h6 style='text-align: center;'>Response Variable</h6>"
                f"<h2 style='text-align: center;'>{response_variable}</h2></div>", unsafe_allow_html=True)

# Second column: Three containers for donut chart and response details
with col2:
    # Container for Donut Chart
    st.markdown("<div class='donut-container'><h4 style='text-align: center;'>Attrition Distribution</h4>", unsafe_allow_html=True)
    
    attrition_counts = df['Attrition'].value_counts().reset_index()
    attrition_counts.columns = ['Attrition', 'Count']
    
    donut_chart = alt.Chart(attrition_counts).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field='Count', type='quantitative'),
        color=alt.Color(field='Attrition', type='nominal', 
                    scale=alt.Scale(domain=['Stayed', 'Left'], 
                                    range=['#00b3b3', '#ff6666']),  # Custom colors for each category
                    legend=alt.Legend(title="Attrition Status")), 
        tooltip=['Attrition', 'Count']
    ).properties(width=200, height=200).configure(background='#2b2b55')
    
    st.altair_chart(donut_chart, theme=None, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Calculate counts and percentages for response variable
    total_count = attrition_counts['Count'].sum()
    
    # Container for First Response Category Details
    first_response_category = attrition_counts.iloc[0]
    percentage_first = (first_response_category['Count'] / total_count) * 100
    
    st.markdown("<div class='response-container'><h5 style='text-align: center;'><strong>{}</strong></h5>"
                f"<h3 style='text-align: center;'>{first_response_category['Count']} <br> ({percentage_first:.2f}%) </h3></div>".format(first_response_category['Attrition']), unsafe_allow_html=True)

    # Container for Second Response Category Details
    second_response_category = attrition_counts.iloc[1]
    percentage_second = (second_response_category['Count'] / total_count) * 100
    
    st.markdown("<div class='response-container'><h5 style='text-align: center;'><strong>{}</strong></h5>"
                f"<h3 style='text-align: center;'>{second_response_category['Count']} <br> ({percentage_second:.2f}%) </h3></div>".format(second_response_category['Attrition']), unsafe_allow_html=True)
    
# Third column of charts in one container
with col3:
    st.markdown("<div class='chart-container'><h4 style='text-align: center;'>Categorical Variable Distribution</h4></div>", unsafe_allow_html=True)
    
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
    ).properties(width=300, height=300
    ).configure(background='#2b2b55')
    
    st.altair_chart(bar_chart, theme=None, use_container_width=True)

    # Chart 3: Numerical Variable Distribution - Histogram with Filter
    st.markdown("<div class='chart-container'><h4 style='text-align: center;'>Numerical Variable Distribution</h4></div>", unsafe_allow_html=True)
    
    numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    selected_num_var = st.selectbox("Select Numerical Variable:", numerical_cols)
    
    histogram = alt.Chart(df).mark_bar().encode(
        x=alt.X(selected_num_var, bin=True),
        y='count()',
        tooltip=[selected_num_var, 'count()']
    ).properties(width=300, height=300
    ).configure(background='#2b2b55')
    
    st.altair_chart(histogram, theme=None, use_container_width=True)


# Fourth column of charts in one container
with col4:
    st.markdown("<div class='chart-container'><h4 style='text-align: center;'>Response vs Categorical Variable</h4></div>", unsafe_allow_html=True)
    
    selected_cat_var_2 = st.selectbox("Select Categorical Variable for Stacked Bar Chart:", categorical_cols)
    
    stacked_data = df.groupby([selected_cat_var_2, 'Attrition']).size().reset_index(name='Count')
    
    stacked_bar_chart = alt.Chart(stacked_data).mark_bar().encode(
        x=alt.X(selected_cat_var_2),
        y='Count',
        color=alt.Color('Attrition:N', legend=None),
        tooltip=[selected_cat_var_2, 'Attrition', 'Count']
    ).properties(width=300, height=300).configure_mark(
        opacity=0.8,
        strokeWidth=0
    ).configure(background='#2b2b55')
    
    st.altair_chart(stacked_bar_chart, theme=None, use_container_width=True)

    # Chart 5: Box Plot for Response vs Numerical Variable
    st.markdown("<div class='chart-container'><h4 style='text-align: center;'>Response vs Numerical Variable</h4></div>", unsafe_allow_html=True)
    
    selected_num_var_2 = st.selectbox("Select Numerical Variable for Box Plot:", numerical_cols)
    
    box_plot = alt.Chart(df).mark_boxplot().encode(
        x=alt.X('Attrition:N'),
        y=alt.Y(selected_num_var_2),
        tooltip=['Attrition', selected_num_var_2]
    ).properties(width=300, height=300
    ).configure(background='#2b2b55')
    
    st.altair_chart(box_plot, theme=None, use_container_width=True)

st.write("")
