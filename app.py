import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. Page Configuration
st.set_page_config(page_title="Virtual Physics Lab", layout="wide")

st.title("⚡ Virtual Electromagnetism Lab")
st.markdown("### Experiment 1: Verification of Ohm's Law")

# 2. Sidebar for Controls (Input)
st.sidebar.header("Lab Equipment Controls")
voltage = st.sidebar.slider("Variable DC Power Supply (V)", 0.0, 20.0, 5.0, 0.1)
resistance = st.sidebar.slider("Resistor Value (Ω)", 10, 1000, 100, 10)

# 3. Physics Logic
current = voltage / resistance  # I = V / R

# 4. Display "Digital Meters"
col1, col2, col3 = st.columns(3)
col1.metric("Voltmeter Reading", f"{voltage} V")
col2.metric("Resistance", f"{resistance} Ω")
col3.metric("Ammeter Reading", f"{current:.4f} A", delta=None)

# 5. Data Visualization (The Graph)
st.subheader("V-I Characteristic Curve")
v_range = np.linspace(0, 20, 100)
i_range = v_range / resistance

fig = go.Figure()
fig.add_trace(go.Scatter(x=v_range, y=i_range, mode='lines', name='Theoretical'))
fig.add_trace(go.Scatter(x=[voltage], y=[current], mode='markers', 
                         marker=dict(size=15, color='red'), name='Current Measurement'))

fig.update_layout(xaxis_title="Voltage (V)", yaxis_title="Current (A)")
st.plotly_chart(fig, use_container_width=True)

st.info("Note: In a real lab, internal resistance of the ammeter would slightly affect these readings.")
