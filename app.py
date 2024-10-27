import streamlit as st
import pandas as pd
import altair as alt

# Set the theme to dark
st.set_page_config(page_title="Employee Attrition Dashboard", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
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
.box3 { background-color: #2eb8b8; color:#000000;}
.box4 { background-color: #71dada;color: #000000; }

.container {
    padding: 10px;  /* Reduced padding */
    border-radius: 0px;
    height: 160px; /* Adjust height to auto for flexibility */
    color: white; /* Text color */
    margin: 5px;  /* Reduced margin */
}
.donut-container {
    padding: 10px;  /* Reduced padding */
    border-radius: 0px;
}
.chart-container {
    padding: 10px;  /* Reduced padding */
    border-radius: 0px;
}

.stSelectbox {
    transition: background-color 0.3s;
    line-height: 50px;
    height: 100px; 
    text-align: center;
    background-color: #3c3c44; /* Change this to your desired color */
    border-radius: 0px; /* Optional: rounded corners */
    padding-left: 10px; /* Optional: padding inside the selectbox */
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
st.write(" ")

# Create columns with different widths
col1, col2, col3, col4 = st.columns(4)  

# First column: Metrics containers stacked vertically
with col1:
    st.markdown("<div class='donut-container'><h5 style='text-align: center;'>Input Parameters</h5></div>", unsafe_allow_html=True)
    st.markdown("<div class='donut-container'>", unsafe_allow_html=True)
    selectbox_style = """
    <div style='background-color: #3c3c44; padding: 10px;'>
        <h6 style='margin: 10; padding: 10px;text-align: center;'>Bar Chart 1 & Stack Bar Chart 1 Parameters</h6>
        <p style="font-size:14px; margin: 10;text-align: center;">Select Categorical Variable</p>
    </div>
    """
    st.markdown(selectbox_style, unsafe_allow_html=True)
    cat_var = st.selectbox("", options=df.select_dtypes(include='object').columns)

    selectbox_style = """
    <div style='background-color: #3c3c44; padding: 10px;'>
        <h6 style='margin: 10; padding: 10px;text-align: center;'>Bar Chart 2 & Stack Bar Chart 2 Parameters</h6>
        <p style="font-size:14px; margin: 10;text-align: center;">Select Numerical Variable</p>
    </div>
    """
    st.markdown(selectbox_style, unsafe_allow_html=True)
    num_var = st.selectbox("", options=df.select_dtypes(include='number').columns)

# Second column: Three containers for donut chart and response details
with col2:
    # Container for Donut Chart
    st.markdown("<div class='donut-container'><h5 style='text-align: center;'>Response Variable Distribution</h5>", unsafe_allow_html=True)
    
    # Calculate response variable distribution
    response_data = df["Attrition"].value_counts().reset_index()
    response_data.columns = ["Attrition", "Count"]
    response_data['Percentage'] = (response_data['Count'] / response_data['Count'].sum()) * 100

    # Donut chart base
    donut_chart = alt.Chart(response_data).mark_arc(innerRadius=60).encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color('Attrition:N', scale=alt.Scale(domain=['Left', 'Stayed'], range=['#FF6347', '#4682B4']),
                    legend=alt.Legend(orient="top", direction="horizontal")),
        tooltip=["Attrition", "Count"]
    ).properties(width=30, height=300)

    # Center text overlay (total count)
    total_count = response_data["Count"].sum()
    center_text = alt.Chart(pd.DataFrame({'text': [total_count]})).mark_text(
        text=str(total_count),
        size=28,
        color='white'
    ).encode(
        text='text:N'
    )
    
    # Combine the donut chart with center text and segment labels
    response_donut_chart = donut_chart + center_text
    
    st.altair_chart(response_donut_chart, theme=None, use_container_width=True)
    
    # Add labels for Left and Stayed categories
    response_data = df["Attrition"].value_counts().reset_index()
    response_data.columns = ["Attrition", "Count"]
    response_data['Percentage'] = (response_data['Count'] / response_data['Count'].sum()) * 100

    # Extracting details for each category
    left_count = response_data.loc[response_data['Attrition'] == 'Left', 'Count'].values[0]
    left_percentage = response_data.loc[response_data['Attrition'] == 'Left', 'Percentage'].values[0]
    
    stayed_count = response_data.loc[response_data['Attrition'] == 'Stayed', 'Count'].values[0]
    stayed_percentage = response_data.loc[response_data['Attrition'] == 'Stayed', 'Percentage'].values[0]

    # Displaying labels
    st.markdown(f"<h5 style='text-align: left;font-size: 12px;margin-top: -220px;'>Stayed<br>{stayed_count}<br>({stayed_percentage:.1f}%)</h5>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align: right;font-size: 12px;margin-top: -180px;'>Left<br>{left_count}<br>({left_percentage:.1f}%)</h5>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    
# Third column of charts in one container
with col3:
    st.markdown("<div class='chart-container'><h5 style='text-align: center;'>Categorical Variable Distribution</h5>", unsafe_allow_html=True)
    
    cat_data = df[cat_var].value_counts().reset_index()
    cat_data.columns = [cat_var, "Count"]
    cat_chart = alt.Chart(cat_data).mark_bar(color='#80bfff').encode(
        x=alt.X(cat_var, sort="-y"),
        y="Count:Q",
        tooltip=[cat_var, "Count"]
    ).properties(width=300, height=300)
 
    st.altair_chart(cat_chart, theme=None, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
    
# Fourth column of charts in one container
with col4:
    st.markdown("<div class='chart-container'><h5 style='text-align: center;'>Numerical Variables Distribution</h5>", unsafe_allow_html=True)
    
    num_chart = alt.Chart(df).mark_bar(color='#80bfff').encode(
        x=alt.X(num_var, bin=True),
        y='count()',
        tooltip=[num_var, 'count()']
    ).properties(width=300, height=300)

    st.altair_chart(num_chart, theme=None, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
    
# Additional Row for New Graphs
col5, col6, col7, col8 = st.columns(4)  

    
with col6:
    st.markdown("<div class='chart-container'><h5 style='text-align: center;'>Data Preview</h5>", unsafe_allow_html=True)
    st.dataframe(df.dropna(how='all').head(6), height=300)
    st.markdown("</div>", unsafe_allow_html=True)
    
with col7:
    st.markdown("<div class='chart-container'><h5 style='text-align: center;'>Response vs Categorical Variables</h5>", unsafe_allow_html=True)

    # Response vs Categorical Variable (Stacked Bar Chart) with custom colors
    stacked_cat_chart = alt.Chart(df).mark_bar().encode(
        y=alt.Y(cat_var, title=cat_var, sort='-x'),
        x=alt.X('count()', title='Count'),
        color=alt.Color('Attrition', scale=alt.Scale(domain=['Left', 'Stayed'], range=['#FF6347', '#4682B4']),
                    legend=alt.Legend(orient="top", direction="horizontal")),
        tooltip=[cat_var, 'Attrition', 'count()']
    ).properties(width=300, height=300)

    st.altair_chart(stacked_cat_chart, theme=None, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
# Fourth column of charts in one container
with col8:
    st.markdown("<div class='chart-container'><h5 style='text-align: center;'>Response vs Numerical Variables</h5>", unsafe_allow_html=True)
    
    # Calculate necessary quantiles and IQR for numerical variable
    q1 = df[num_var].quantile(0.25)
    q3 = df[num_var].quantile(0.75)
    iqr = q3 - q1

    # Filter outliers
    df_filtered = df[(df[num_var] >= (q1 - 1.5 * iqr)) & (df[num_var] <= (q3 + 1.5 * iqr))]

    # Create Box Plot with white whiskers
    box_plot = alt.Chart(df_filtered).mark_boxplot(size=40, color='white').encode(
        x=alt.X("Attrition:N", title="Attrition"),
        y=alt.Y(num_var, title=num_var),
        color=alt.Color("Attrition", scale=alt.Scale(domain=['Left', 'Stayed'], range=['#FF6347', '#4682B4']),
                    legend=alt.Legend(orient="top", direction="horizontal"))
    ).properties(width=300, height=300)

    st.altair_chart(box_plot, theme=None, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)



