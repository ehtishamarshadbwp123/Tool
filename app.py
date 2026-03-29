import streamlit as st

st.set_page_config(page_title="COCC Frequency System", layout="wide")

# --- Offline-Compatible Professional CSS ---
st.markdown("""
    <style>
    /* Using standard system fonts for 100% offline reliability */
    /* Sans-serif for clean UI, Impact/Arial Black for the "Glow" look */
    
    .stApp { 
        background-color: #05070a; 
        color: #ffffff; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
    }
    
    [data-testid="stSidebar"] { background-color: #0a0e14 !important; border-right: 2px solid #00f2ff; }
    
    .sidebar-name {
        font-family: 'Arial Black', Gadget, sans-serif;
        color: #39ff14; font-size: 1.3rem; font-weight: 700;
        padding: 20px 10px; border-bottom: 2px solid #39ff14;
        text-shadow: 0 0 10px rgba(57, 255, 20, 0.5); text-align: center;
    }

    .stNumberInput div div input {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #00f2ff !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
        font-family: 'Consolas', 'Courier New', monospace !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    div[data-testid="stMarkdownContainer"] p { color: #ffffff !important; font-weight: 500; }
    .stRadio label { color: #ffffff !important; font-size: 0.95rem !important; }
    div[data-baseweb="radio"] div { background-color: #1f2937 !important; border-color: #00f2ff !important; }

    .glow-text { 
        color: #00f2ff; 
        text-shadow: 0 0 15px rgba(0, 242, 255, 0.6); 
        font-family: 'Arial Black', Gadget, sans-serif; 
        font-size: 2.5rem !important; text-align: center; margin-bottom: 10px;
    }

    .stNumberInput label { color: #ffae00 !important; font-weight: 700; text-transform: uppercase; }

    .result-box {
        background: #0d1117;
        border: 2px solid #00f2ff;
        padding: 15px; border-radius: 8px; text-align: center;
        box-shadow: 0 0 10px rgba(0, 242, 255, 0.2);
    }
    .result-box b { 
        color: #39ff14; 
        font-size: 1.3rem; 
        font-family: 'Consolas', 'Courier New', monospace;
    }

    .status-banner {
        background-color: #111; border: 1px solid #30363d;
        padding: 10px 20px; border-radius: 5px; border-left: 5px solid #ffae00;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Initialization (Fixed Startup Error) ---
if 'up' not in st.session_state:
    st.session_state.up, st.session_state.dn = 6225.0, 4000.0
    st.session_state.decim, st.session_state.modem = 1550.0, 1325.0
    st.session_state.last_changed = 'up'
    st.session_state.current_sat = "MM1"
    st.session_state.current_band = "C-BAND"

def update_logic():
    source = st.session_state.get('last_changed', 'up')
    sat = st.session_state.current_sat
    band = st.session_state.current_band
    active_lo = st.session_state.get('lo_sel', 3050)
    
    MODEM_LO = 4900 if band == "C-BAND" else 12800
    DECIM_LO = 2450 if band == "C-BAND" else 9750
    TRANS_LO = 2225 if band == "C-BAND" else active_lo

    if source == 'modem':
        st.session_state.up = st.session_state.modem + MODEM_LO
        st.session_state.dn = st.session_state.up - TRANS_LO
        st.session_state.decim = st.session_state.dn - DECIM_LO
    elif source == 'up':
        st.session_state.dn = st.session_state.up - TRANS_LO
        st.session_state.modem = st.session_state.up - MODEM_LO
        st.session_state.decim = st.session_state.dn - DECIM_LO
    elif source == 'down':
        st.session_state.up = st.session_state.dn + TRANS_LO
        st.session_state.modem = st.session_state.up - MODEM_LO
        st.session_state.decim = st.session_state.dn - DECIM_LO
    elif source == 'decim':
        st.session_state.dn = st.session_state.decim + DECIM_LO
        st.session_state.up = st.session_state.dn + TRANS_LO
        st.session_state.modem = st.session_state.up - MODEM_LO

def main():
    # Sidebar
    st.sidebar.markdown("<div class='sidebar-name'>Ehtisham Arshad</div>", unsafe_allow_html=True)
    st.sidebar.markdown("<h2 style='color:#00f2ff; text-align:center; margin-bottom:0;'>COCC</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='color:#888; text-align:center; font-size:0.8rem; margin-top:0;'>Carrier Operation and Communication Control</p>", unsafe_allow_html=True)
    st.sidebar.write("---")
    st.sidebar.radio("SATELLITE SELECT", ["MM1", "1R"], key="current_sat")
    st.sidebar.radio("BAND SELECT", ["C-BAND", "KU-BAND"], key="current_band")
    
    # Main Header
    st.markdown("<h1 class='glow-text'>FREQUENCY CONVERSION SYSTEM</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='status-banner'><b style='color:#ffae00;'>SYSTEM ACTIVE:</b> {st.session_state.current_sat} | {st.session_state.current_band}</div>", unsafe_allow_html=True)

    main_col, ref_col = st.columns([0.7, 0.3])

    with main_col:
        if st.session_state.current_band == "KU-BAND":
            st.write("### SELECT TRANSLATION OFFSET (LO)")
            options = {2300: "Lower (F1-F6)", 3050: "Standard (F8-F12)", 1550: "Extended (F13-F20)"} if st.session_state.current_sat == "MM1" else {3050: "Standard (Ku1-12)", 1250: "Extended (Ku13-18)"}
            st.radio("", options.keys(), format_func=lambda x: options[x], horizontal=True, key="lo_sel", on_change=update_logic)
        else: st.session_state.lo_sel = 2225

        update_logic()

        up_r = (5900.0, 6500.0) if st.session_state.current_band == "C-BAND" else (12750.0, 14250.0)
        dn_r = (3700.0, 4200.0) if st.session_state.current_band == "C-BAND" else (10700.0, 13000.0)
        dec_r = (1200.0, 1800.0) if st.session_state.current_band == "C-BAND" else (950.0, 3300.0)
        
        c1, c2 = st.columns(2)
        with c1:
            st.caption(f"Range: {up_r[0]} - {up_r[1]} MHz")
            st.number_input("Uplink Center (RF)", up_r[0], up_r[1], key="up", on_change=lambda: st.session_state.update(last_changed='up'))
            st.caption(f"Range: {dec_r[0]} - {dec_r[1]} MHz")
            st.number_input("Decimater (L-Band)", dec_r[0], dec_r[1], key="decim", on_change=lambda: st.session_state.update(last_changed='decim'))
        with c2:
            st.caption(f"Range: {dn_r[0]} - {dn_r[1]} MHz")
            st.number_input("Downlink Center (RF)", dn_r[0], dn_r[1], key="dn", on_change=lambda: st.session_state.update(last_changed='down'))
            st.caption(f"Range: 950 - 2150 MHz")
            st.number_input("Modem (L-Band)", 950.0, 2150.0, key="modem", on_change=lambda: st.session_state.update(last_changed='modem'))

        bw = st.number_input("Bandwidth (MHz)", 0.1, 100.0, 36.0)
        sym_rate = (bw / 1.2) * 1000
        st.info(f"CALCULATED SYMBOL RATE: {sym_rate:.2f} ksps")

    with ref_col:
        st.markdown("<h3 style='color:#39ff14;'>QUICK REF</h3>", unsafe_allow_html=True)
        if st.session_state.current_band == "KU-BAND":
            if st.session_state.current_sat == "MM1":
                ref_html = """<div style='border:1px solid #39ff14; padding:10px; font-size:0.85rem;'>
                <b>MM1 Ku-Band Details:</b><br><br>
                - <b>Lower (F1-F6):</b><br>Range: 13000-13250 | <b>LO: 2300</b><br><br>
                - <b>Standard (F8-F12):</b><br>Range: 14000-14250 | <b>LO: 3050</b><br><br>
                - <b>Extended (F13-F20):</b><br>Range: 12750-13000 | <b>LO: 1550</b>
                </div>"""
            else:
                ref_html = """<div style='border:1px solid #39ff14; padding:10px; font-size:0.85rem;'>
                <b>1-R Ku-Band Details:</b><br><br>
                - <b>Standard (Ku1-12):</b><br>Range: 13750-14000 | <b>LO: 3050</b><br><br>
                - <b>Extended (Ku13-18):</b><br>Range: 14000-14250 | <b>LO: 1250</b>
                </div>"""
        else:
            ref_html = "<div style='border:1px solid #39ff14; padding:10px;'><b>C-Band Standard:</b><br>Up: 5.9-6.5 GHz<br>Dn: 3.7-4.2 GHz<br>LO: 2225</div>"
        st.markdown(ref_html, unsafe_allow_html=True)

    st.write("### SPECTRUM RANGE")
    v1, v2, v3 = st.columns(3)
    v1.markdown(f"<div class='result-box'><small>UPLINK</small><br><b>{st.session_state.up-(bw/2):.2f}-{st.session_state.up+(bw/2):.2f}</b></div>", unsafe_allow_html=True)
    v2.markdown(f"<div class='result-box'><small>DOWNLINK</small><br><b>{st.session_state.dn-(bw/2):.2f}-{st.session_state.dn+(bw/2):.2f}</b></div>", unsafe_allow_html=True)
    v3.markdown(f"<div class='result-box'><small>L-DEC</small><br><b>{st.session_state.decim-(bw/2):.2f}-{st.session_state.decim+(bw/2):.2f}</b></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()