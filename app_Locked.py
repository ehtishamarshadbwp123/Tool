import streamlit as st

st.set_page_config(page_title="COCC Frequency System", layout="wide")

# --- CSS: RESTORED HOVER, CONTRAST & BRANDING ---
st.markdown("""
    <style>
    .stApp { background-color: #05070a; color: #ffffff; font-family: 'Arial', sans-serif; }
    [data-testid="stSidebar"] { background-color: #0a0e14 !important; border-right: 2px solid #00f2ff; }
    .sidebar-name {
        font-family: 'Arial Black', sans-serif;
        color: #39ff14; font-size: 1.3rem; font-weight: 700;
        padding: 20px 10px; border-bottom: 2px solid #39ff14;
        text-shadow: 0 0 10px rgba(57, 255, 20, 0.5); text-align: center;
    }
    .stNumberInput div div input {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #00f2ff !important;
        font-size: 1.6rem !important;
        font-weight: bold !important;
        font-family: 'Consolas', monospace !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    div[data-testid="stWidgetLabel"] p, .stRadio label, div[role="radiogroup"] label p { 
        color: #ffffff !important; font-weight: 700 !important; 
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.2);
    }
    .glow-text { 
        color: #00f2ff; text-shadow: 0 0 15px rgba(0, 242, 255, 0.6); 
        font-family: 'Arial Black', sans-serif; font-size: 3.2rem !important; text-align: center;
    }
    .stNumberInput label { color: #ffae00 !important; font-weight: 700; text-transform: uppercase; }
    .result-box {
        background: #0d1117; border: 2px solid #00f2ff;
        padding: 15px; border-radius: 8px; text-align: center;
        box-shadow: 0 0 10px rgba(0, 242, 255, 0.2);
    }
    .result-box b { color: #39ff14; font-size: 1.3rem; font-family: 'Consolas', monospace; }
    .section-header {
        color: #ffae00; font-weight: 800; font-size: 1.2rem;
        border-left: 5px solid #ffae00; padding: 5px 15px; margin-top: 25px; margin-bottom: 15px;
        background: rgba(255, 174, 0, 0.05);
    }
    .stTooltipIcon { color: #00f2ff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- Initialization ---
if 'up' not in st.session_state:
    st.session_state.up, st.session_state.dn = 6137.5, 3912.5
    st.session_state.decim, st.session_state.modem = 1462.5, 1237.5
    st.session_state.last_changed = 'up'
    st.session_state.current_sat, st.session_state.current_band = "MM1", "C-BAND"

def update_logic():
    source = st.session_state.get('last_changed', 'up')
    band = st.session_state.current_band
    sat = st.session_state.current_sat
    
    # Get the raw value from the radio button
    raw_lo = st.session_state.get('lo_sel', 2225)
    
    # Mapping dictionary - Updated to match your exact radio button labels
    lo_map = {
        "Lower (F1-F6)": 2300.0,
        "Standard (F8-F12)": 3050.0,
        "Extended (F13-F20)": 1550.0,
        "Standard (Ku1-12)": 3050.0,
        "Extended (Ku13-18)": 1250.0,
        "Standard (Ku.1-Ku.6)": 3050.0,  # Added for 1-R compatibility
        "Extended (Ku.7-Ku.20)": 1250.0   # Added for 1-R compatibility
    }

    # SAFE LOOKUP: Check the dictionary first. 
    # If not found, only then try to convert to float.
    if isinstance(raw_lo, str):
        if raw_lo in lo_map:
            active_lo = lo_map[raw_lo]
        else:
            # Fallback if a string is passed that isn't in the map
            active_lo = 3050.0 
    else:
        active_lo = float(raw_lo)
    
    # Constants
    MODEM_LO = 4900.0 if band == "C-BAND" else 12800.0
    DECIM_LO = 2450.0 if band == "C-BAND" else 9750.0
    TRANS_LO = 2225.0 if band == "C-BAND" else active_lo
    
    # Core Math Logic
    if source == 'modem':
        st.session_state.up = float(st.session_state.modem) + MODEM_LO
        st.session_state.dn = st.session_state.up - TRANS_LO
        st.session_state.decim = st.session_state.dn - DECIM_LO
    elif source == 'up':
        st.session_state.dn = float(st.session_state.up) - TRANS_LO
        st.session_state.modem = st.session_state.up - MODEM_LO
        st.session_state.decim = st.session_state.dn - DECIM_LO
    elif source == 'down':
        st.session_state.up = float(st.session_state.dn) + TRANS_LO
        st.session_state.modem = st.session_state.up - MODEM_LO
        st.session_state.decim = st.session_state.dn - DECIM_LO
    elif source == 'decim':
        st.session_state.dn = float(st.session_state.decim) + DECIM_LO
        st.session_state.up = st.session_state.dn + TRANS_LO
        st.session_state.modem = st.session_state.up - MODEM_LO

def main():
    # --- Sidebar Branding (RESTORED FULL COCC NAME) ---
    st.sidebar.markdown("<div class='sidebar-name'>Ehtisham Arshad</div>", unsafe_allow_html=True)
    st.sidebar.markdown("""
    <h2 style='color:#00f2ff; text-align:center; margin-bottom:0; font-size: 3.5rem; font-family: "Arial Black", sans-serif; text-shadow: 0 0 10px rgba(0, 242, 255, 0.5);'>
        COCC
    </h2>
    <div style='background-color: #00f2ff; height: 5px; width: 80%; margin: 0 auto; box-shadow: 0 0 10px rgba(0, 242, 255, 0.5); border-radius: 2px;'></div>
    <h2 style='color:#888; text-align:center; font-size:1.2rem; margin-top:10px; font-weight:normal;'>Carrier Operation and Communication Control</h2>
    """, unsafe_allow_html=True)
    st.sidebar.write("---")
    st.sidebar.radio("SATELLITE SELECT", ["MM1", "1R"], key="current_sat", on_change=update_logic)
    st.sidebar.radio("BAND SELECT", ["C-BAND", "KU-BAND"], key="current_band", on_change=update_logic)
# Main Header
    st.markdown("<h1 class='glow-text'>FREQUENCY CONVERSION SYSTEM</h1>", unsafe_allow_html=True)

    # --- Feature 1: Main Conversion Section ---
    st.markdown("<div class='section-header'>1. MAIN FREQUENCY CONVERSION</div>", unsafe_allow_html=True)
    
    main_col, ref_col = st.columns([0.7, 0.3])

    with main_col:
        # KU-Band LO Selection Logic
        if st.session_state.current_band == "KU-BAND":
            st.write("### SELECT TRANSLATION OFFSET (LO)")
            if st.session_state.current_sat == "MM1":
                options = {2300: "Lower (F1-F6)", 3050: "Standard (F8-F12)", 1550: "Extended (F13-F20)"}
            else: # 1-R
                options = {3050: "Standard (Ku.1-Ku.6)", 1250: "Extended (Ku.7-Ku.20)"}
            
            st.radio("", options.keys(), format_func=lambda x: options[x], horizontal=True, key="lo_sel", on_change=update_logic)
        else:
            st.session_state.lo_sel = 2225 # Fixed C-Band LO

        update_logic()

        # --- Dynamic Range Constraints (Strictly enforced for input and hover) ---
        if st.session_state.current_band == "C-BAND":
            up_r, dn_r, dec_r = (5850.0, 6425.0), (3625.0, 4200.0), (1175.0, 1750.0)
        else: # KU-BAND
            lo = st.session_state.get('lo_sel', 3050)
            if st.session_state.current_sat == "MM1":
                if lo == 2300: up_r, dn_r, dec_r = (13000.0, 13250.0), (10700.0, 10950.0), (950.0, 1200.0)
                elif lo == 3050: up_r, dn_r, dec_r = (14000.0, 14250.0), (10950.0, 11200.0), (1200.0, 1450.0)
                else: up_r, dn_r, dec_r = (12750.0, 13000.0), (11200.0, 11450.0), (1450.0, 1700.0)
            else: # 1-R
                if lo == 3050: up_r, dn_r, dec_r = (14000.0, 14250.0), (10950.0, 11200.0), (1200.0, 1450.0)
                else: up_r, dn_r, dec_r = (13750.0, 14000.0), (12500.0, 12750.0), (2750.0, 3000.0)

        c1, c2 = st.columns(2)
        with c1:
            st.number_input("Uplink Center (RF)", up_r[0], up_r[1], key="up", help=f"Restrictive Range: {up_r[0]} - {up_r[1]} MHz", step=0.001, format="%.3f", on_change=lambda: st.session_state.update(last_changed='up'))
            st.number_input("Decimater (L-Band)", dec_r[0], dec_r[1], key="decim", help=f"Restrictive Range: {dec_r[0]} - {dec_r[1]} MHz", step=0.001, format="%.3f", on_change=lambda: st.session_state.update(last_changed='decim'))
        with c2:
            st.number_input("Downlink Center (RF)", dn_r[0], dn_r[1], key="dn", help=f"Restrictive Range: {dn_r[0]} - {dn_r[1]} MHz", step=0.001, format="%.3f", on_change=lambda: st.session_state.update(last_changed='down'))
            
            if st.session_state.current_band == "C-BAND":
                st.number_input("Modem (L-Band)", 950.0, 2150.0, key="modem", help="Range: 950 - 2150 MHz", step=0.001, format="%.3f", on_change=lambda: st.session_state.update(last_changed='modem'))
            else:
                st.info("Modem calculation moved to Section 3.")

    with ref_col:
        # --- RESTORED QUICK REF HTML ---
        st.markdown("<h3 style='color:#39ff14; text-align:center;'>QUICK REF</h3>", unsafe_allow_html=True)
        if st.session_state.current_band == "KU-BAND":
            if st.session_state.current_sat == "MM1":
                ref_html = f"""<div style='border:1px solid #39ff14; padding:10px; font-size:0.85rem;'>
                <b>MM1 Ku-Band:</b><br><br>
                - <b>Lower (F1-F6):</b><br>Up: 13000-13250<br>Dn: 10700-10950<br>LO: 2300<br><br>
                - <b>Standard (F8-F12):</b><br>Up: 14000-14250<br>Dn: 10950-11200<br>LO: 3050<br><br>
                - <b>Extended (F13-F20):</b><br>Up: 12750-13000<br>Dn: 11200-11450<br>LO: 1550
                </div>"""
            else: # 1-R
                ref_html = f"""<div style='border:1px solid #39ff14; padding:10px; font-size:0.85rem;'>
                <b>1-R Ku-Band:</b><br><br>
                - <b>Standard (Ku.1-6):</b><br>Up: 14000-14250<br>Dn: 10950-11200<br>LO: 3050<br><br>
                - <b>Extended (Ku.7-20):</b><br>Up: 13750-14000<br>Dn: 12500-12750<br>LO: 1250
                </div>"""
        else:
            ref_html = """<div style='border:1px solid #39ff14; padding:15px; text-align:center;'>
            <b>C-Band Standard</b><br><br>Up: 5850 - 6425<br>Dn: 3625 - 4200<br>Dec: 1175 - 1750<br>LO: 2225<br>Modem LO: 4900</div>"""
        st.markdown(ref_html, unsafe_allow_html=True)
# --- Feature 2: Symbol Rate & Spectrum Section ---
    st.markdown("<div class='section-header'>2. SYMBOL RATE & SPECTRUM RANGE</div>", unsafe_allow_html=True)
    bw = st.number_input("Bandwidth (MHz)", 0.1, 250.0, 36.0, step=0.1, help="Enter occupied BW (Range: 0.1 - 250 MHz)")
    sym_rate = (bw / 1.2) * 1000
    
    v0, v1, v2, v3 = st.columns(4)
    v0.markdown(f"<div class='result-box'><small>SYMBOL RATE</small><br><b>{sym_rate:.2f} ksps</b></div>", unsafe_allow_html=True)
    v1.markdown(f"<div class='result-box'><small>UPLINK RANGE</small><br><b>{st.session_state.up-(bw/2):.3f}-{st.session_state.up+(bw/2):.3f}</b></div>", unsafe_allow_html=True)
    v2.markdown(f"<div class='result-box'><small>DOWNLINK RANGE</small><br><b>{st.session_state.dn-(bw/2):.3f}-{st.session_state.dn+(bw/2):.3f}</b></div>", unsafe_allow_html=True)
    v3.markdown(f"<div class='result-box'><small>L-DECIMATER</small><br><b>{st.session_state.decim-(bw/2):.3f}-{st.session_state.decim+(bw/2):.3f}</b></div>", unsafe_allow_html=True)

    # --- Feature 3: Dynamic Section Numbering & LO Note ---
    if st.session_state.current_band == "KU-BAND":
        st.markdown("<div class='section-header'>3. KU-BAND LO CALCULATOR</div>", unsafe_allow_html=True)
        
        # Mapping for the Note to show the specific Band Name
        lo_selection = st.session_state.get('lo_sel', 3050)
        if st.session_state.current_sat == "MM1":
            band_note = {2300: "Lower (F1-F6)", 3050: "Standard (F8-F12)", 1550: "Extended (F13-F20)"}.get(lo_selection, "Standard")
        else:
            band_note = {3050: "Standard (Ku.1-Ku.6)", 1250: "Extended (Ku.7-Ku.20)"}.get(lo_selection, "Standard")
            
        st.warning(f"⚠️ Active Logic: **{band_note}**. Ensure your Input RF matches the selected toggle in Section 1.")
        
        l1, l2, l3 = st.columns(3)
        rf_in = l1.number_input("Input RF Uplink", up_r[0], up_r[1], value=up_r[0], format="%.3f", key="lo_rf_in", help=f"Enter RF (Range: {up_r[0]}-{up_r[1]})")
        custom_lo = l2.number_input("Custom LO (e.g. 12800)", 1.0, 20000.0, value=12800.0, help="Enter your Local Oscillator Frequency")
        l3.markdown(f"<div class='result-box'><small>L-BAND MODULATOR</small><br><b>{abs(rf_in - custom_lo):.3f} MHz</b></div>", unsafe_allow_html=True)
        
        sec_num = "4"
    else:
        # If C-Band, this becomes Section 3
        sec_num = "3"

    # --- Feature 4: Bandwidth (Start/Stop) Calculator ---
    st.markdown(f"<div class='section-header'>{sec_num}. BANDWIDTH & SPAN CALCULATOR</div>", unsafe_allow_html=True)
    calc_mode = st.radio("Select Target Field", ["RF Uplink", "RF Downlink", "L-Band Decimater"], horizontal=True)
    
    if "Uplink" in calc_mode: current_r = up_r
    elif "Downlink" in calc_mode: current_r = dn_r
    else: current_r = dec_r

    b1, b2, b3, b4 = st.columns(4)
    start_f = b1.number_input("Start Frequency", current_r[0], current_r[1], value=current_r[0], format="%.3f", key="calc_start_f", help=f"Start Freq for {calc_mode}")
    stop_f = b2.number_input("Stop Frequency", current_r[0], current_r[1], value=current_r[1], format="%.3f", key="calc_stop_f", help=f"Stop Freq for {calc_mode}")
    
    b3.markdown(f"<div class='result-box'><small>CENTER FREQUENCY</small><br><b>{(start_f + stop_f)/2:.3f}</b></div>", unsafe_allow_html=True)
    b4.markdown(f"<div class='result-box'><small>SPAN (BANDWIDTH)</small><br><b>{abs(stop_f - start_f):.3f} MHz</b></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
