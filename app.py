import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Load Data
df = pd.read_csv("Nifty_Stocks.csv")
df['Date'] = pd.to_datetime(df['Date'])

# Sidebar Filters
st.sidebar.title("📊 Stock Filter")

# Category selection
categories = df['Category'].unique()
selected_category = st.sidebar.selectbox("Select Category", categories)

# Symbol selection (based on category)
filtered_df = df[df['Category'] == selected_category]
symbols = filtered_df['Symbol'].unique()
selected_symbol = st.sidebar.selectbox("Select Stock Symbol", symbols)

# Filtered data for the selected symbol
final_df = filtered_df[filtered_df['Symbol'] == selected_symbol]

# Date Range Selector
min_date = final_df['Date'].min()
max_date = final_df['Date'].max()
date_range = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)
final_df = final_df[(final_df['Date'] >= pd.to_datetime(date_range[0])) &
                    (final_df['Date'] <= pd.to_datetime(date_range[1]))]

# Moving Average
ma_days = st.sidebar.slider("Moving Average Window (days)", 1, 50, 10)
final_df['MA'] = final_df['Close'].rolling(ma_days).mean()

# Chart Type Selection
chart_type = st.sidebar.radio("Chart Type", ["Line Chart", "Candlestick"])

# Title
st.title("📈 Nifty Stock Price Dashboard")
st.write(f"### {selected_symbol} - Close Price from {date_range[0]} to {date_range[1]}")

# Plotting
if chart_type == "Line Chart":
    fig, ax = plt.subplots(figsize=(10, 5))
    sb.lineplot(x=final_df['Date'], y=final_df['Close'], label="Close", ax=ax)
    sb.lineplot(x=final_df['Date'], y=final_df['MA'], label=f"{ma_days}-day MA", ax=ax)
    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.title(f"{selected_symbol} - Close Price & MA")
    st.pyplot(fig)

elif chart_type == "Candlestick":
    fig = go.Figure(data=[go.Candlestick(
        x=final_df['Date'],
        open=final_df['Open'],
        high=final_df['High'],
        low=final_df['Low'],
        close=final_df['Close']
    )])
    fig.update_layout(title=f"{selected_symbol} - Candlestick Chart",
                      xaxis_rangeslider_visible=False)
    st.plotly_chart(fig)

# Download Button
csv_data = final_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv_data,
    file_name=f"{selected_symbol}_data.csv",
    mime="text/csv"
)

