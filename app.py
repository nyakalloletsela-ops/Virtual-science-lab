import streamlit as st

st.sidebar.title("🧰 Digital Storeroom")
topic = st.sidebar.selectbox("Select Lab Module", 
                             ["Electricity & Magnetism", "Motion", "Waves", "Thermal Physics"])

if topic == "Electricity & Magnetism":
    st.header("⚡ Electricity Workbench")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Apparatus Selection")
        # Define Voltage based on battery selection
        battery_choice = st.radio("Pick a Battery Source", 
                                 ["1.5V Cell", "3.0V (2x Cells in Series)", "9V Battery"])
        
        voltage_map = {"1.5V Cell": 1.5, "3.0V (2x Cells in Series)": 3.0, "9V Battery": 9.0}
        V = voltage_map[battery_choice]
        
        # Define Resistance
        load_choice = st.selectbox("Select Load Component", ["10Ω Resistor", "Small Lightbulb (3V Max)"])
        R = 10 if load_choice == "10Ω Resistor" else 5  # Lightbulb has lower resistance

    with col2:
        st.subheader("Workbench Status")
        current = V / R
        
        # Real-world behavior logic
        if load_choice == "Small Lightbulb (3V Max)" and V > 3.0:
            st.error("💥 POP! The bulb filament snapped. Too much voltage!")
            st.metric("Ammeter Reading", "0.0 A")
        else:
            status = "💡 The bulb is glowing brightly!" if load_choice == "Small Lightbulb (3V Max)" else "✅ Circuit is closed."
            st.success(status)
            st.metric("Ammeter Reading", f"{current:.2f} A")
            st.write(f"**Mathematical Proof:** $I = \\frac{V}{R} = \\frac{{ {V} }}{{ {R} }} = {current:.2f} A$")

# Placeholder for your next module
elif topic == "Motion":
    st.header("🏎️ Mechanics Lab")
    st.info("Coming soon: Ticker Timer and Friction experiments.")
