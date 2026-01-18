import streamlit as st
import pandas as pd
import time
import random
import numpy as np
from datetime import datetime
from fpdf import FPDF # The PDF Library

# --- CONFIGURATION ---
RVCE_LAT = 12.9240
RVCE_LON = 77.4990
APP_NAME = "Namma Report"

# --- PAGE SETUP ---
st.set_page_config(page_title=APP_NAME, layout="wide", page_icon="🇮🇳")

# --- SESSION STATE ---
if 'reports' not in st.session_state: st.session_state.reports = []
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'otp_verified' not in st.session_state: st.session_state.otp_verified = False
if 'otp_sent' not in st.session_state: st.session_state.otp_sent = False
if 'current_otp' not in st.session_state: st.session_state.current_otp = 0

# --- 📄 REAL PDF GENERATOR FUNCTION ---
def create_pdf(ticket):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"BBMP / RVCE Smart City Report", ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt=f"Official Incident Report: #{ticket['id']}", ln=True, align='L')
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Date Reported: {ticket['timestamp']}", ln=True)
    pdf.cell(200, 10, txt=f"Category: {ticket['category']}", ln=True)
    pdf.cell(200, 10, txt=f"Priority: {ticket['priority']}", ln=True)
    pdf.cell(200, 10, txt=f"Location: {ticket['lat']}, {ticket['lon']}", ln=True)
    pdf.cell(200, 10, txt=f"Current Status: {ticket['status']}", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 11)
    pdf.multi_cell(0, 10, txt=f"AI Analysis Reason: {ticket['reason']}")
    
    pdf.ln(20)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(200, 10, txt="Authorized Signature: _______________________", ln=True)
    pdf.cell(200, 10, txt="Ward Officer, Rajarajeshwari Nagar", ln=True)
    
    return pdf.output(dest='S').encode('latin-1')

# --- AI SIMULATION ---
def analyze_image_simulation(image_file):
    name = image_file.name.lower()
    if "pothole" in name:
        return "Major Asphalt Deterioration", "High", "Severity Level 4 crater; exposed aggregate base. Immediate risk to 2-wheelers."
    elif "garbage" in name or "dump" in name:
        return "Illegal Waste Accumulation", "Medium", "Mixed solid waste pile (>50kg). vector breeding risk. Requires sanitation crew."
    elif "light" in name or "pole" in name:
        return "Streetlight Infrastructure Failure", "Medium", "Pole #RV-402 luminaire broken. Electrical safety hazard & reduced visibility."
    elif "pipe" in name or "water" in name:
        return "Potable Water Main Rupture", "High", "Significant treated water loss on main supply line. Risk of road undercut erosion."
    elif "traffic" in name:
        return "High Density Congestion", "Low", "V/C Ratio > 1.2 at junction. Signal cycle optimization recommended."
    else:
        return "Unclassified Civic Anomaly", "Low", "Non-critical issue detected. Queued for manual inspection."

# --- SIDEBAR ---
st.sidebar.title(APP_NAME)
st.sidebar.markdown("Developing Bengalauru, Together.")
page = st.sidebar.radio("Select Portal", ["📱 Citizen Reporting App", "🚔 Official Admin Dashboard"])

# ================= VIEW 1: CITIZEN APP =================
if page == "📱 Citizen Reporting App":
    st.title(f"🇮🇳 {APP_NAME} - Citizen Portal")
    
    # LOGIN
    if not st.session_state.otp_verified:
        with st.container(border=True):
            st.subheader("🔐 Secure Login (MFA)")
            phone = st.text_input("Mobile Number (+91)", max_chars=10)
            if st.button("Request OTP 🔑"):
                if len(phone)==10:
                    st.session_state.otp_sent = True
                    st.session_state.current_otp = random.randint(1000, 9999)
                    with st.spinner("Encrypted handshake with SMS gateway..."):
                        time.sleep(1.2)
                    st.toast(f"SIMULATION: Your OTP is {st.session_state.current_otp}", icon="💬")
                    st.info(f"💡 Demo OTP sent to {phone}")
            if st.session_state.otp_sent:
                if st.button("Verify & Access") or st.text_input("OTP", type="password") == str(st.session_state.current_otp):
                    st.session_state.otp_verified = True
                    st.rerun()

    # REPORTING
    else:
        st.success("👤 Verified Resident ID: RVCE-UG-2024")
        if st.button("🔄 Logout"): st.session_state.otp_verified=False; st.rerun()
        st.divider()
        with st.form("report_form", clear_on_submit=True):
            st.subheader("📸 New Incident Report")
            uploaded_file = st.file_uploader("Upload Evidence", type=['jpg','png','jpeg'])
            st.success(f"📍 Locked Coordinates: {RVCE_LAT}, {RVCE_LON} (RVCE Campus Geo-Fence)")
            if st.form_submit_button("🚀 Submit Report"):
                if uploaded_file:
                    with st.spinner("☁️ Running Cloud AI Vision Model..."):
                        time.sleep(1.5)
                        cat, prio, reason = analyze_image_simulation(uploaded_file)
                    new_report = {
                        "id": f"TKT-{random.randint(10000, 99999)}",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "category": cat, "priority": prio, "reason": reason,
                        "lat": RVCE_LAT, "lon": RVCE_LON, "status": "Open"
                    }
                    st.session_state.reports.append(new_report)
                    st.balloons()
                    st.success(f"✅ Ticket #{new_report['id']} Generated: {cat}")

# ================= VIEW 2: ADMIN DASHBOARD =================
elif page == "🚔 Official Admin Dashboard":
    if not st.session_state.logged_in:
        st.title("🔒 Ward Command Center")
        user = st.text_input("Officer ID"); pwd = st.text_input("Password", type="password")
        if st.button("Secure Login 🛡️") and user=="admin" and pwd=="admin":
            st.session_state.logged_in = True; st.rerun()
    else:
        st.sidebar.divider()
        st.sidebar.metric("Live IoT Sensors", "8 Units Online", delta="Active")
        if st.sidebar.button("🛑 Sign Out"): st.session_state.logged_in=False; st.rerun()

        st.title("🚔 Bengaluru Smart City - Triage Dashboard")
        
        # TABS
        tab1, tab2 = st.tabs(["📋 Ticket Management", "📡 IoT Sensor Hub"])

        with tab1:
            if st.session_state.reports:
                df = pd.DataFrame(st.session_state.reports)
                
                # 1. THE DATA TABLE
                def style_priority(val):
                    if val == 'High': return 'background-color: #ffcccb; color: darkred; font-weight: bold'
                    if val == 'Medium': return 'background-color: #fff4cc; color: darkorange'
                    return 'color: green'
                st.dataframe(df[["id","category","priority","status","timestamp"]].style.map(style_priority, subset=['priority']), use_container_width=True)
                
                st.divider()
                
                # 2. THE MANAGEMENT PANEL (Update Status + Download PDF)
                st.subheader("🛠️ Ticket Actions")
                
                col_select, col_action, col_pdf = st.columns([2, 2, 2])
                
                with col_select:
                    # Dropdown to select a ticket ID
                    ticket_ids = df['id'].tolist()
                    selected_id = st.selectbox("Select Ticket ID", ticket_ids)
                
                # Get the actual ticket object
                selected_ticket = next((item for item in st.session_state.reports if item["id"] == selected_id), None)
                
                with col_action:
                    # Dropdown to change status
                    new_status = st.selectbox("Update Status", ["Open", "In Progress", "Resolved", "Rejected"], index=0)
                    if st.button("Update Status & Notify User"):
                        # Update the "Database"
                        for ticket in st.session_state.reports:
                            if ticket['id'] == selected_id:
                                ticket['status'] = new_status
                        
                        st.success(f"Status updated to: {new_status}")
                        # SMS SIMULATION
                        st.toast(f"📲 SMS Sent to User: 'Your Ticket {selected_id} is now {new_status}'", icon="📨")
                        time.sleep(1)
                        st.rerun()

                with col_pdf:
                    # REAL PDF DOWNLOAD
                    if selected_ticket:
                        st.write("###") # Spacer
                        pdf_data = create_pdf(selected_ticket)
                        st.download_button(
                            label="📄 Download Official PDF Report",
                            data=pdf_data,
                            file_name=f"Report_{selected_id}.pdf",
                            mime="application/pdf"
                        )

            else:
                st.info("No tickets in queue.")

        with tab2:
            st.subheader("📡 Real-time Environmental Data (RVCE Campus)")
            col1, col2 = st.columns(2)
            chart_data_aqi = pd.DataFrame(np.random.randint(60, 150, size=(20, 1)), columns=['AQI (PM2.5)'])
            col1.line_chart(chart_data_aqi, color="#00ff00")
            col1.caption("Air Quality: Moderate")
            
            chart_data_noise = pd.DataFrame(np.random.randint(40, 85, size=(20, 1)), columns=['Noise Level (dB)'])
            col2.area_chart(chart_data_noise, color="#3366ff")
            col2.caption("Noise Levels: Normal")