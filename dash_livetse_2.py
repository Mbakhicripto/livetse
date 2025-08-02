import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.tse_tools import *  # Replace with your own module

# Load data
df = get_all_market('stocks')

# Rename columns for consistency
df = df.rename(columns={
    'symbol': 'Symbol',
    'close_price': 'Close Price',
    'value': 'Trade Value',
    'volume': 'Trade Volume',
    'number_trades': 'Trades Count',
    'first_price': 'First Price',
    'last_trade': 'Last Trade',
    'low_price': 'Low Price',
    'high_price': 'High Price',
    'yesterday_price': 'Yesterday Price',
    'eps': 'EPS',
    'base_volume': 'Base Volume',
    'max_allowed_price': 'Max Price',
    'min_allowed_price': 'Min Price',
    'number_shares': 'Shares Outstanding'
})

# Layout settings
st.set_page_config(layout="wide", page_title="Live Market Dashboard", page_icon="📊")
st.markdown("""
    <style>
    .main {
        background-color: #f9f9f9;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Live Market Intelligence Dashboard")
st.markdown("A modern, professional dashboard for real-time stock monitoring.")

col1, col2, col3 = st.columns(3)

# Market Breadth
positive = (df['Close Price'].diff() > 0).sum()
negative = (df['Close Price'].diff() < 0).sum()
with col1:
    st.metric("Gainers", positive)
with col2:
    st.metric("Losers", negative)
with col3:
    st.metric("Breadth Ratio", f"{positive / (negative + 1):.2f}")

st.markdown("---")

# Chart 1: First vs Last Price Ratio
st.subheader("🟦 First vs Last Trade Price Ratio")
df['Price Movement Ratio'] = df['Last Trade'] / (df['First Price'] + 1)
fig_power = px.bar(df.sort_values('Price Movement Ratio', ascending=False).head(20),
                   x='Symbol', y='Price Movement Ratio', color='Price Movement Ratio',
                   color_continuous_scale='Bluered_r',
                   labels={'Price Movement Ratio': 'Last/First Price'})
st.plotly_chart(fig_power, use_container_width=True)

# Chart 2: Trade Value Leaderboard
st.subheader("💸 Top Symbols by Trade Value")
fig_money = px.bar(df.sort_values('Trade Value', ascending=False).head(15),
                   x='Symbol', y='Trade Value', color='Trade Value',
                   color_continuous_scale='Tealrose')
st.plotly_chart(fig_money, use_container_width=True)

# Chart 3: Price Range (High vs Low)
st.subheader("📊 Daily Price Range")
df['Range'] = df['High Price'] - df['Low Price']
fig_range = px.bar(df.sort_values('Range', ascending=False).head(15),
                   x='Symbol', y='Range', color='Range',
                   color_continuous_scale='Agsunset')
st.plotly_chart(fig_range, use_container_width=True)

# Chart 4: Scatter Plot - Close Price vs Trade Value
st.subheader("🔎 Close Price vs Trade Value")
fig_bubble = px.scatter(df, x='Close Price', y='Trade Value',
                        size='Trade Volume', color='Symbol',
                        hover_name='Symbol', size_max=60)
st.plotly_chart(fig_bubble, use_container_width=True)

# Chart 5: EPS vs Close Price
st.subheader("🏆 EPS vs Close Price")
fig_eps = px.scatter(df[df['EPS'] > 0], x='EPS', y='Close Price', color='Symbol',
                     hover_name='Symbol', size='Shares Outstanding', size_max=60)
st.plotly_chart(fig_eps, use_container_width=True)

st.markdown("---")

# Additional Chart: Trade Value by Type of Asset
st.subheader("🏦 Trade Value by Type of Asset")
for asset_type in df['type_of_asset'].dropna().unique():
    df_category = df[df['type_of_asset'] == asset_type].sort_values('Trade Value', ascending=False).head(15)
    st.markdown(f"**📂 {asset_type}**")
    fig_asset = px.bar(df_category, x='Symbol', y='Trade Value', color='Trade Value',
                       color_continuous_scale='Sunsetdark')
    st.plotly_chart(fig_asset, use_container_width=True)

st.caption("© 2025 bakhezri Company | Powered by Live Market Data")
