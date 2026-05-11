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
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import warnings
import logging

st.set_page_config(page_title="Wealth Engineering Engine", layout="wide")

# ANSI Color logic converted to Streamlit
def color_text(text, color):
    colors = {"G": "green", "R": "red", "W": "black", "B": "blue", "Y": "orange"}
    return f":{colors.get(color, 'black')}[{text}]"

st.title("✅ WEALTH ENGINEERING: DYNAMIC CATALYST ENGINE")

# --- 1. Portfolio Basis & Pivot (User Inputs) ---
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
    mechanical_shield_pct = st.number_input("Mechanical Shield % (Trailing Stop)", value=12)

# --- Logic Engines ---
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
        base_indices = ['SPY', 'QQQ', 'DIA', 'IWM']
        sector_map = {
            'Technology': ['SMH', 'NVDA', 'PLTR', 'SOUN'],
            'Industrials': ['XLI', 'VRT', 'ETN', 'POWL'],
            'Consumer Cyclical': ['TSLA', 'AMZN', 'META', 'DKNG'],
            'Financial Services': ['XLF', 'SOFI', 'UPST', 'COIN']
        }
        sector = info.get('sector', 'Technology')
        peers = base_indices + sector_map.get(sector, sector_map['Technology'])
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
        color = "green" if change > 0.05 else "red" if change < -0.05 else "black"
        return last, change, emoji, color
    except: return 0.0, 0.0, "❂", "black"

# --- Execution ---
if st.button("RUN INSTITUTIONAL AUDIT"):
    organic_base = current_portfolio_value - injection_amt
    days_passed = (datetime.datetime.now().date() - pivot_start_date).days
    true_velocity = ((organic_base / pivot_start_value) - 1) / max(1, days_passed)

    strike_name, peer_chain, live_high, is_strike_ticker_valid = get_dynamic_audit_data(strike_ticker)

    if is_strike_ticker_valid:
        strike_p, strike_c, strike_e, strike_clr = get_snapshot(strike_name)
        vwap, obv_s, is_trend_strong = get_trend_indicators(strike_name)
        shield_floor_price = live_high * (1 - (mechanical_shield_pct / 100))
        if price_reaction == "Runaway Trend":
            shield_floor_price = max(shield_floor_price, strike_p * 0.96)

        is_shield_breached = strike_p <= shield_floor_price

        if is_shield_breached:
            tactical_signal = "☣ MARKET SELL (SHIELD BREACHED)"
            sig_col = "red"
        elif price_reaction == "Runaway Trend":
            if is_trend_strong:
                tactical_signal = "🚀 TREND DAY EXPLOITATION: HOLD (ABOVE VWAP + OBV RISING)"
                sig_col = "blue"
            else:
                tactical_signal = "⚠️ TREND WEAKENING: HARVEST IMMEDIATELY"
                sig_col = "red"
        elif harvesting_engine_on:
            tactical_signal = "💰 HARVEST / TAKE PROFITS" if strike_c > 5 else "✅ HOLD / MONITOR"
            sig_col = "green"
        else:
            tactical_signal = "✅ HOLD / MONITOR"
            sig_col = "green"

        st.subheader(f"☇ INSTITUTIONAL AUDIT: {strike_name}")
        st.metric(label=f"{strike_e} PRICE", value=f"${strike_p:.2f}", delta=f"{strike_c:.2f}%")
        
        col1, col2 = st.columns(2)
        if vwap:
            col1.write(f"**VWAP:** ${vwap:.2f}")
            col1.write(f"**OBV SLOPE:** {'POSITIVE' if obv_s > 0 else 'NEGATIVE'}")
        
        shield_status = "ACTIVE" if not is_shield_breached else "BREACHED"
        col2.write(f"**SHIELD:** :{ 'green' if not is_shield_breached else 'red' }[{shield_status}]")
        col2.write(f"**FLOOR:** ${shield_floor_price:.2f}")

        if price_reaction == "Runaway Trend":
            st.error("🚨 PROTOCOL ALERT: CLOSING AUCTION TIME-STOP ACTIVE 🚨")
            st.warning(f"☣️ MANDATORY LIQUIDATION: 3:50 PM EST (MARKET ON CLOSE) ☣️\n\nREASON: +{strike_c:.2f}% ANOMALY DETECTED. AVOID OVER-NIGHT VOLATILITY CRUSH.")

        st.write("---")
        st.write(f"### SYMPATHETIC CHAIN FOR {strike_name}")
        peer_cols = st.columns(4)
        for i, peer in enumerate(peer_chain):
            p_p, p_c, p_e, p_clr = get_snapshot(peer)
            peer_cols[i % 4].metric(label=f"{p_e} {peer}", value=f"${p_p:.2f}", delta=f"{p_c:.2f}%")

        st.write("---")
        st.write(f"**TRUE VELOCITY:** {true_velocity*100:.4f}% per session")
        st.subheader(f"TACTICAL SIGNAL: :{sig_col}[{tactical_signal}]")
        st.write("---")

        st.write("### WEALTH TRAJECTORY PROJECTIONS (ACTUAL VELOCITY)")
        goals = [100000, 300000, 750000]
        for g in goals:
            if g <= current_portfolio_value:
                st.write(f"❉ ${g/1000:.0f}K: REACHED")
                continue
            if true_velocity > 0:
                target_ratio = g / current_portfolio_value
                sessions = np.log(target_ratio) / np.log(1 + true_velocity)
                proj_date = pivot_start_date + datetime.timedelta(days=int(sessions))
                date_str = proj_date.strftime("%Y-%m-%d")
                st.write(f"❉ ${g/1000:.0f}K: Need ${g - current_portfolio_value:,.2f} | Est: **{sessions:.1f} sessions** ({date_str})")
            else:
                st.write(f"❉ ${g/1000:.0f}K: Need ${g - current_portfolio_value:,.2f} | Est: N/A")
    else:
        st.error(f"Invalid Ticker: {strike_ticker}")
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
