import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import datetime

st.set_page_config(page_title="Wealth Engineering Engine", layout="wide")
st.title("✅ WEALTH ENGINEERING: DYNAMIC CATALYST ENGINE")

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("1. Portfolio Basis")
    # Using defaults of 0 or empty strings to make it truly dynamic/user-driven
    current_val = st.number_input("Current Portfolio Value", min_value=0.0, step=100.0)
    pivot_date = st.date_input("Pivot Start Date", value=datetime.date.today())
    pivot_val = st.number_input("Pivot Start Value", min_value=0.0, step=100.0)
    injection = st.number_input("Non-Organic Funds", min_value=0.0, step=100.0)

    st.header("2. Strike Harvester")
    ticker = st.text_input("Strike Ticker (e.g., AAPL, NVDA, INOD)").upper()
    reaction = st.selectbox("Price Reaction", ["Flat or Dropped", "Gapped Up", "Gapped Down", "Runaway Trend"])
    
    st.header("3. Augmentations")
    shield_pct = st.slider("Mechanical Shield %", 0, 100, 12)

# --- Engine Logic ---
@st.cache_data(ttl=600)
def get_audit(ticker_symbol):
    if not ticker_symbol:
        return None, None, None
    try:
        t = yf.Ticker(ticker_symbol)
        hist = t.history(period='1mo')
        if hist.empty:
            return None, None, None
        
        last = hist['Close'].iloc[-1]
        prev_close = hist['Close'].iloc[-2]
        chg = ((last / prev_close) - 1) * 100
        high_52 = hist['High'].max()
        return last, chg, high_52
    except Exception:
        return None, None, None

if st.button("RUN INSTITUTIONAL AUDIT"):
    if not ticker:
        st.warning("Please enter a ticker symbol in the sidebar.")
    else:
        with st.spinner(f"Analyzing {ticker}..."):
            price, change, high_52 = get_audit(ticker)
        
        if price is not None:
            st.metric(label=f"LIVE PRICE: {ticker}", value=f"${price:.2f}", delta=f"{change:.2f}%")

            if reaction == "Runaway Trend":
                st.error("🚨 PROTOCOL ALERT: CLOSING AUCTION TIME-STOP ACTIVE")
                st.warning("MANDATORY LIQUIDATION: 3:50 PM EST (MARKET ON CLOSE)")

            # Calculated logic example
            velocity = ((price - pivot_val) / pivot_val * 100) if pivot_val > 0 else 0
            st.write(f"### Engine Analysis")
            col1, col2 = st.columns(2)
            col1.metric("Pivot Velocity", f"{velocity:.2f}%")
            col2.metric("Shield Adjusted Value", f"${(current_val * (1 - shield_pct/100)):.2f}")
            
            st.info(f"Analysis complete for {ticker} based on a ${current_val} portfolio baseline.")
        else:
            st.error(f"Could not retrieve data for '{ticker}'. Check the symbol or try again later.")
