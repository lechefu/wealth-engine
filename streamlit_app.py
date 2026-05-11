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
    current_val = st.number_input("Current Portfolio Value", value=47907)
    pivot_date = st.text_input("Pivot Start Date", "2026-04-28")
    pivot_val = st.number_input("Pivot Start Value", value=31071.20)
    injection = st.number_input("Non-Organic Funds", value=10000.0)

    st.header("2. Strike Harvester")
    ticker = st.text_input("Strike Ticker", "INOD").upper()
    reaction = st.selectbox("Price Reaction", ["Flat or Dropped", "Gapped Up", "Gapped Down", "Runaway Trend"])
    
    st.header("3. Augmentations")
    shield_pct = st.slider("Mechanical Shield %", 0, 30, 12)

# --- Engine Logic ---
def get_audit(ticker_symbol):
    t = yf.Ticker(ticker_symbol)
    hist = t.history(period='5d')
    last = hist['Close'].iloc[-1]
    chg = ((last / hist['Close'].iloc[-2]) - 1) * 100
    return last, chg, t.info.get('fiftyTwoWeekHigh', last)

if st.button("RUN INSTITUTIONAL AUDIT"):
    price, change, high_52 = get_audit(ticker)
    
    # Display Metric
    st.metric(label=f"LIVE PRICE: {ticker}", value=f"${price:.2f}", delta=f"{change:.2f}%")

    if reaction == "Runaway Trend":
        st.error("🚨 PROTOCOL ALERT: CLOSING AUCTION TIME-STOP ACTIVE")
        st.warning("MANDATORY LIQUIDATION: 3:50 PM EST (MARKET ON CLOSE)")

    st.info(f"True Velocity and Projections would calculate here using ${current_val} base.")
