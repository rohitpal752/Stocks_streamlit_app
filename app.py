import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("Nifty_Stocks.csv")
df['Date'] = pd.to_datetime(df['Date'])

# Sidebar - Category selection
st.sidebar.title("Stock Filter")
categories = df['Category'].unique()
selected_category = st.sidebar.selectbox("Select Category", categories)

# Filter symbols based on selected category
filtered_df = df[df['Category'] == selected_category]
symbols = filtered_df['Symbol'].unique()
selected_symbol = st.sidebar.selectbox("Select Stock Symbol", symbols)

# Final filtered data
final_df = filtered_df[filtered_df['Symbol'] == selected_symbol]

# Title
st.title("📈 Nifty Stock Price Dashboard")
st.write(f"### Showing Close Price for `{selected_symbol}` under `{selected_category}` category")

# Plotting
fig, ax = plt.subplots(figsize=(10, 5))
sb.lineplot(x=final_df['Date'], y=final_df['Close'], ax=ax)
plt.xticks(rotation=45)
plt.xlabel("Date")
plt.ylabel("Close Price")
plt.title(f"{selected_symbol} - Close Price Over Time")
st.pyplot(fig)
