import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import warnings
import logging

# 1. Setup Page (Only once!)
st.set_page_config(page_title="Wealth Engineering Engine", layout="wide")
st.title("✅ WEALTH ENGINEERING: DYNAMIC CATALYST ENGINE")

# --- 2. Sidebar Inputs ---
with st.sidebar:
    st.header("1. Portfolio Basis & Pivot")
    current_portfolio_value = st.number_input("Current Portfolio Value", value=47907.0)
    pivot_start_date = st.date_input("Pivot Start Date", value=datetime.date(2026, 4, 28))
    pivot_start_value = st.number_input("Pivot Start Value", value=31071.20)
    injection_amt = st.number_input("Non-Organic Funds", value=10000.00)

    st.header("2. The Strike Harvester")
    strike_ticker = st.text_input("Strike Ticker", value="INOD").upper()
    catalyst_news = st.selectbox("Catalyst News", ["Beat / Good Guidance", "Miss / Poor Guidance", "Neutral", "Pending / Not Yet Released"], index=0)
    price_reaction = st.selectbox("Price Reaction", ["Flat or Dropped", "Gapped Up", "Gapped Down", "Runaway Trend"], index=3)

    st.header("3. Functional Augmentations")
    harvesting_engine_on = st.checkbox("Harvesting Engine On", value=False)
    mechanical_shield_pct = st.number_input("Mechanical Shield % (Trailing Stop)", value=12.0)

# --- 3. Logic Engines ---
def get_trend_indicators(ticker_symbol):
    try:
        t = yf.Ticker(ticker_symbol)
        df = t.history(period="1d", interval="5m")
        if df.empty: return None, None, False
        df['VWAP'] = (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()
        current_vwap = df['VWAP'].iloc[-1]
        df['OBV'] = (np.sign(df['Close'].diff()) * df['Volume']).fillna(0).cumsum()
        obv_slope = df['OBV'].tail(5).diff().mean()
        is_strong = (df['Close'].iloc[-1] > current_vwap) and (obv_slope > 0)
        return current_vwap, obv_slope, is_strong
    except: return None, None, False

def get_dynamic_audit_data(ticker_input):
    raw_t = ticker_input.upper().strip()
    t = yf.Ticker(raw_t)
    info = t.info
    history = t.history(period="1d")
    is_valid = not (not info or history.empty)
    peers = []
    high_52w = 0.0
    if is_valid:
        sector_map = {
            'Technology': ['SMH', 'NVDA', 'PLTR', 'SOUN'],
            'Industrials': ['XLI', 'VRT', 'ETN', 'POWL'],
            'Consumer Cyclical': ['TSLA', 'AMZN', 'META', 'DKNG'],
            'Financial Services': ['XLF', 'SOFI', 'UPST', 'COIN']
        }
        sector = info.get('sector', 'Technology')
        peers = ['SPY', 'QQQ', 'DIA', 'IWM'] + sector_map.get(sector, sector_map['Technology'])
        peers = [p for p in peers if p != raw_t][:8]
        high_52w = info.get('fiftyTwoWeekHigh', 0.0)
    return raw_t, peers, high_52w, is_valid

def get_snapshot(ticker):
    try:
        t = yf.Ticker(ticker)
        data = t.history(period="5d")
        last, prev = data['Close'].iloc[-1], data['Close'].iloc[-2]
        change = ((last / prev) - 1) * 100
        emoji = "✅" if change > 0.05 else "❃" if change < -0.05 else "❂"
        return last, change, emoji
    except: return 0.0, 0.0, "❂"

# --- 4. Execution ---
if st.button("RUN INSTITUTIONAL AUDIT"):
    organic_base = current_portfolio_value - injection_amt
    days_passed = (datetime.datetime.now().date() - pivot_start_date).days
    true_velocity = ((organic_base / pivot_start_value) - 1) / max(1, days_passed)

    strike_name, peer_chain, live_high, is_valid = get_dynamic_audit_data(strike_ticker)

    if is_valid:
        strike_p, strike_c, strike_e = get_snapshot(strike_name)
        vwap, obv_s, is_trend_strong = get_trend_indicators(strike_name)
        shield_floor = live_high * (1 - (mechanical_shield_pct / 100))
        
        if price_reaction == "Runaway Trend":
            shield_floor = max(shield_floor, strike_p * 0.96)

        st.subheader(f"☇ INSTITUTIONAL AUDIT: {strike_name}")
        st.metric(label=f"{strike_e} PRICE", value=f"${strike_p:.2f}", delta=f"{strike_c:.2f}%")
        
        col1, col2 = st.columns(2)
        if vwap:
            col1.write(f"**VWAP:** ${vwap:.2f} | **OBV:** {'POS' if obv_s > 0 else 'NEG'}")
        
        status = "ACTIVE" if strike_p > shield_floor else "BREACHED"
        col2.write(f"**SHIELD:** {status} | **FLOOR:** ${shield_floor:.2f}")

        if price_reaction == "Runaway Trend":
            st.error("🚨 PROTOCOL ALERT: CLOSING AUCTION TIME-STOP ACTIVE")
            st.warning("☣️ MANDATORY LIQUIDATION: 3:50 PM EST (MARKET ON CLOSE)")

        st.write("---")
        st.write("### SYMPATHETIC CHAIN")
        peer_cols = st.columns(4)
        for i, peer in enumerate(peer_chain):
            p_p, p_c, p_e = get_snapshot(peer)
            peer_cols[i % 4].metric(label=f"{p_e} {peer}", value=f"${p_p:.2f}", delta=f"{p_c:.2f}%")

        st.write("---")
        st.write(f"**TRUE VELOCITY:** {true_velocity*100:.4f}% per session")
        
        st.write("### WEALTH TRAJECTORY PROJECTIONS")
        goals = [100000, 300000, 750000]
        for g in goals:
            if g <= current_portfolio_value:
                st.write(f"❉ ${g/1000:.0f}K: REACHED")
            elif true_velocity > 0:
                sessions = np.log(g / current_portfolio_value) / np.log(1 + true_velocity)
                st.write(f"❉ ${g/1000:.0f}K: Est. **{sessions:.1f} sessions**")
    else:
        st.error(f"Invalid Ticker: {strike_ticker}")
