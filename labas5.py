import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Oil Price Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown(
    """
    <style>
    .css-18e3th9 {background-color: #f0f2f6;} /* Main background */
    .css-1d391kg {background-color: #1f77b4; color: white;} /* Sidebar */
    .css-1v3fvcr {color: #333333;} /* Text color */
    </style>
    """,
    unsafe_allow_html=True
)


st.title("Oil Price Visualization Dashboard")


@st.cache_data
def load_data():
    url_brent = "https://raw.githubusercontent.com/datasets/oil-prices/master/data/brent-daily.csv"
    url_wti = "https://raw.githubusercontent.com/datasets/oil-prices/master/data/wti-daily.csv"
    brent_df = pd.read_csv(url_brent)
    wti_df = pd.read_csv(url_wti)
    brent_df['Date'] = pd.to_datetime(brent_df['Date'])
    wti_df['Date'] = pd.to_datetime(wti_df['Date'])
    brent_df['Type'] = 'Brent'
    wti_df['Type'] = 'WTI'
    return pd.concat([brent_df, wti_df])

df = load_data()


st.sidebar.header("Filter Options")
start_date = st.sidebar.date_input("Start Date", df['Date'].min())
end_date = st.sidebar.date_input("End Date", df['Date'].max())

filtered_df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]


st.subheader("WTI vs Brent Oil Prices Over Time")
fig_line = px.line(filtered_df, x='Date', y='Price', color='Type',
                   title="WTI vs Brent Oil Prices Over Time",
                   labels={'Price': 'Price (USD)', 'Date': 'Date'},
                   color_discrete_map={'Brent': '#00A19C', 'WTI': '#ff7f0e'})
st.plotly_chart(fig_line, use_container_width=True)


st.subheader("Average Monthly Brent Oil Prices")
brent_filtered = filtered_df[filtered_df['Type'] == 'Brent']
brent_filtered['Month'] = brent_filtered['Date'].dt.to_period('M')
monthly_avg = brent_filtered.groupby('Month')['Price'].mean().reset_index()
monthly_avg['Month'] = monthly_avg['Month'].astype(str)
fig_bar = px.bar(monthly_avg, x='Month', y='Price',
                 title="Average Monthly Brent Oil Prices",
                 labels={'Price': 'Average Price (USD)', 'Month': 'Month'},
                 color='Price', color_continuous_scale='Viridis')
fig_bar.update_traces(marker_line_color='green', marker_line_width=1.5)
st.plotly_chart(fig_bar, use_container_width=True)


st.subheader("Price Distribution Histogram")
fig_hist = px.histogram(filtered_df, x='Price', nbins=30, color='Type',
                        title="Distribution of WTI and Brent Oil Prices",
                        labels={'Price': 'Price (USD)'},
                        color_discrete_map={'Brent': '#763F98', 'WTI': '#20419A'})
fig_hist.update_traces(marker_line_color='black', marker_line_width=1.2)
st.plotly_chart(fig_hist, use_container_width=True)


if st.checkbox("Show Raw Data"):
    st.write(filtered_df)
