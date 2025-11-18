import streamlit as st
import pandas as pd
import plotly.express as px

st.title("COVID-19 Data Visualization Dashboard")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv"
    df = pd.read_csv(url)
    df['Date'] = pd.to_datetime(df['Date'])
    return df 


df = load_data()

st.sidebar.header("Filter Options")
country = st.sidebar.selectbox("Select Country", df['Country'].unique())
metric = st.sidebar.radio("Select Metric", ['Confirmed', 'Recovered', 'Deaths'])
filtered_df = df[df['Country'] == country]

fig = px.line(filtered_df, x='Date', y=metric, title=f"{metric} Cases in {country}")
st.plotly_chart(fig, use_container_width=True)
if st.checkbox("Show Raw Data"):
    st.write(filtered_df)
